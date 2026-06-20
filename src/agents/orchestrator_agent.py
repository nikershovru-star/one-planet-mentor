"""
orchestrator_agent.py — AI-оркестратор на Hermes3
Принимает решения о маршрутизации запросов между агентами
"""

import os
import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from .base_agent import BaseAgent
from ..models import AgentContext


class OrchestratorAgent(BaseAgent):
    """
    AI-оркестратор на Hermes3.
    Анализирует запрос и решает какие агенты вызвать.
    """
    
    def __init__(self):
        super().__init__("orchestrator_agent")
        model = os.getenv("ORCHESTRATOR_MODEL", "hermes3:8b")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.2
        )
    
    async def get_context(self, query: str, age: int, religion: str) -> AgentContext:
        """Анализирует запрос и возвращает план выполнения."""
        
        # ВАЖНО: фигурные скобки в JSON экранированы двойными {{}}
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — AI-оркестратор One Planet Mentor.
Твоя задача: проанализировать запрос пользователя и определить план выполнения.

ДОСТУПНЫЕ АГЕНТЫ:
1. age_agent — адаптация под возраст (5-99 лет)
2. faith_agent — религиозный контекст (7 традиций)
3. science_agent — научные ответы
4. safety_agent — проверка безопасности

ПРИНЦИПЫ:
- Планетарная идентичность первична
- Религия вторична, но уважаема
- Безопасность всегда проверяется первой
- Возраст определяет стиль ответа

Отвечай в формате JSON:
{{
  "needs_safety_check": true,
  "needs_age_adaptation": true,
  "needs_faith_context": false,
  "primary_agent": "science_agent",
  "complexity": "medium",
  "estimated_tokens": 500
}}

Отвечай ТОЛЬКО JSON, без пояснений."""),
            ("user", """Возраст пользователя: {age}
Религиозный контекст: {religion}
Запрос: {query}""")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "age": age,
            "religion": religion,
            "query": query
        })
        
        # Парсим JSON из ответа
        try:
            text = response.content.strip()
            # Убираем markdown обёртку если есть
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            plan = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            # Fallback если JSON не распарсился
            plan = {
                "needs_safety_check": True,
                "needs_age_adaptation": True,
                "needs_faith_context": religion != "unspecified",
                "primary_agent": "science_agent",
                "complexity": "medium",
                "estimated_tokens": 500
            }
        
        return AgentContext(
            agent_name="orchestrator_agent",
            guidelines=json.dumps(plan, ensure_ascii=False),
            metadata=plan
        )
    
    async def decide_routing(self, query: str, age: int, religion: str) -> dict:
        """Упрощённый метод для быстрого роутинга."""
        context = await self.get_context(query, age, religion)
        return context.metadata