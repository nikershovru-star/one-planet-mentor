"""
career_agent.py — Агент карьеры и профориентации
Помогает с выбором профессии, развитием навыков, карьерным ростом
Учитывает язык пользователя
"""

import os
import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from .base_agent import BaseAgent
from ..models import AgentContext


class CareerAgent(BaseAgent):
    """Эксперт по карьере, профориентации и развитию навыков."""
    
    def __init__(self):
        super().__init__("career_agent")
        model = os.getenv("CAREER_AGENT_MODEL", "qwen3:14b")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.4
        )
    
    async def get_context(self, age: int, query: str, goals: list = None) -> AgentContext:
        """Анализирует карьерный запрос и даёт рекомендации."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — карьерный консультант One Planet Mentor.
Помогаешь людям найти свой путь, развить навыки, построить карьеру.

ПРИНЦИПЫ:
- Учитывай возраст и этап жизни
- Давай конкретные, выполнимые советы
- Подчёркивай важность непрерывного обучения
- Уважай разные пути (не только корпоративный)
- Планетарный взгляд: карьера может служить миру

Формат ответа (JSON):
{{
  "career_stage": "student|entry|mid|senior|transition|retirement",
  "recommended_skills": ["навык1", "навык2"],
  "action_steps": ["шаг1", "шаг2", "шаг3"],
  "resources": ["ресурс1", "ресурс2"],
  "planetary_connection": "как это служит миру"
}}

Отвечай ТОЛЬКО JSON."""),
            ("user", """Возраст: {age}
Цели пользователя: {goals}
Запрос: {query}""")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "age": age,
            "goals": ", ".join(goals) if goals else "не указаны",
            "query": query
        })
        
        try:
            text = response.content.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            career_data = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            career_data = {
                "career_stage": "unknown",
                "recommended_skills": [],
                "action_steps": [],
                "resources": [],
                "planetary_connection": ""
            }
        
        return AgentContext(
            agent_name="career_agent",
            guidelines=json.dumps(career_data, ensure_ascii=False),
            metadata=career_data
        )
    
    async def answer(self, query: str, age: int, goals: list = None, language: str = "ru") -> str:
        """Даёт развёрнутый карьерный совет на языке пользователя."""
        
        lang_names = {
            "ru": "русском",
            "en": "английском",
            "es": "испанском",
            "fr": "французском",
            "de": "немецком",
            "zh": "китайском",
            "ar": "арабском",
            "hi": "хинди",
            "pt": "португальском",
            "ja": "японском"
        }
        
        target_lang = lang_names.get(language, "русском")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — опытный карьерный консультант One Planet Mentor.

ВОЗРАСТ ПОЛЬЗОВАТЕЛЯ: {age}
ЦЕЛИ: {goals}

ВАЖНО: Отвечай СТРОГО на {target_lang} языке!

ПРАВИЛА:
- Давай конкретные, выполнимые советы
- Учитывай этап жизни
- Подчёркивай важность обучения
- В конце добавь как это служит миру (планетарный мостик)
- Будь вдохновляющим, но реалистичным
- 200-400 слов"""),
            ("user", "{query}")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "age": age,
            "goals": ", ".join(goals) if goals else "не указаны",
            "target_lang": target_lang,
            "query": query
        })
        
        return response.content
