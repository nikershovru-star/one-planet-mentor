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
    
    async def get_context(self, query: str, age: int, religion: str, user_language: str = "ru") -> AgentContext:
        """Анализирует запрос и возвращает план выполнения."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — AI-оркестратор One Planet Mentor.
Твоя задача: проанализировать запрос пользователя и определить план выполнения.

ДОСТУПНЫЕ ЭКСПЕРТЫ (primary_agent):
- science_agent — научные вопросы, факты, объяснения
- career_agent — карьера, профориентация, навыки, работа
- creative_agent — творчество, истории, стихи, идеи, игры
- wellness_agent — ментальное здоровье, тревога, стресс, медитации
- faith_agent — религиозные вопросы, духовность
- search_agent — актуальные новости, свежие факты, Wikipedia

ДОСТУПНЫЕ КОНТЕКСТНЫЕ АГЕНТЫ:
- age_agent — адаптация под возраст (5-99 лет)
- faith_agent — религиозный контекст
- memory_agent — история диалогов
- search_agent — поиск информации
- wellness_agent — анализ настроения

ПРАВИЛА ВЫБОРА primary_agent:
- "Как работает...", "Что такое...", "Объясни..." → science_agent
- "Как войти в IT", "карьера", "навыки", "работа" → career_agent
- "Напиши историю", "стих", "придумай", "творч" → creative_agent
- "тревога", "стресс", "грусть", "депрессия", "медитация" → wellness_agent
- "Бог", "религия", "вера", "молитва" → faith_agent
- "новости", "последние", "сейчас", "2024", "2025" → search_agent

Отвечай в формате JSON:
{{
  "needs_safety_check": true,
  "needs_age_adaptation": true,
  "needs_faith_context": false,
  "needs_language_processing": false,
  "needs_memory": true,
  "needs_search": false,
  "search_type": "web",
  "needs_wellness": false,
  "primary_agent": "science_agent",
  "secondary_agents": [],
  "complexity": "medium",
  "estimated_tokens": 500
}}

Отвечай ТОЛЬКО JSON, без пояснений."""),
            ("user", """Возраст пользователя: {age}
Религиозный контекст: {religion}
Язык пользователя: {user_language}
Запрос: {query}""")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "age": age,
            "religion": religion,
            "user_language": user_language,
            "query": query
        })
        
        try:
            text = response.content.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            plan = json.loads(text)
        except json.JSONDecodeError:
            plan = {
                "needs_safety_check": True,
                "needs_age_adaptation": True,
                "needs_faith_context": religion != "unspecified",
                "needs_language_processing": False,
                "needs_memory": True,
                "needs_search": False,
                "search_type": "web",
                "needs_wellness": False,
                "primary_agent": "science_agent",
                "secondary_agents": [],
                "complexity": "medium",
                "estimated_tokens": 500
            }
        
        return AgentContext(
            agent_name="orchestrator_agent",
            guidelines=json.dumps(plan, ensure_ascii=False),
            metadata=plan
        )
    
    async def decide_routing(self, query: str, age: int, religion: str, user_language: str = "ru") -> dict:
        """Упрощённый метод для быстрого роутинга."""
        context = await self.get_context(query, age, religion, user_language)
        return context.metadata
