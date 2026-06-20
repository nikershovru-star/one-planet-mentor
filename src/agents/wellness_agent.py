"""
wellness_agent.py — Агент ментального здоровья и благополучия
Поддержка, медитации, работа с тревогой и стрессом
Учитывает язык пользователя
"""

import os
import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from .base_agent import BaseAgent
from ..models import AgentContext


class WellnessAgent(BaseAgent):
    """Агент ментального здоровья и благополучия."""
    
    def __init__(self):
        super().__init__("wellness_agent")
        model = os.getenv("WELLNESS_AGENT_MODEL", "qwen3:14b")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.5
        )
    
    async def get_context(self, age: int, query: str, mood: str = "neutral") -> AgentContext:
        """Анализирует эмоциональное состояние и даёт рекомендации."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — эксперт по ментальному здоровью One Planet Mentor.
Проанализируй эмоциональное состояние пользователя и дай рекомендации.

ПРИНЦИПЫ:
- Будь эмпатичным и поддерживающим
- НЕ ставь диагнозы (ты не врач)
- Предлагай практические техники
- Если серьёзные проблемы — рекомендуй обратиться к специалисту
- Учитывай возраст

Формат (JSON):
{{
  "mood_detected": "anxious|sad|stressed|neutral|happy",
  "severity": "low|medium|high",
  "recommendations": ["техника1", "техника2"],
  "needs_professional_help": false,
  "support_message": "поддерживающее сообщение"
}}

Отвечай ТОЛЬКО JSON."""),
            ("user", """Возраст: {age}
Настроение: {mood}
Запрос: {query}""")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "age": age,
            "mood": mood,
            "query": query
        })
        
        try:
            text = response.content.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            wellness_data = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            wellness_data = {
                "mood_detected": "neutral",
                "severity": "low",
                "recommendations": [],
                "needs_professional_help": False,
                "support_message": ""
            }
        
        return AgentContext(
            agent_name="wellness_agent",
            guidelines=json.dumps(wellness_data, ensure_ascii=False),
            metadata=wellness_data
        )
    
    async def provide_support(self, query: str, age: int, mood: str = "neutral", language: str = "ru") -> str:
        """Даёт развёрнутую поддержку и рекомендации на языке пользователя."""
        
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
            ("system", """Ты — поддерживающий наставник One Planet Mentor.
Помогаешь людям справляться со стрессом, тревогой, грустью.

ВОЗРАСТ: {age}
НАСТРОЕНИЕ: {mood}

ВАЖНО: Отвечай СТРОГО на {target_lang} языке! Будь тёплым и эмпатичным.

ПРАВИЛА:
- Используй техники: дыхание, медитация, заземление
- Давай конкретные упражнения
- Напоминай о важности заботы о себе
- Если серьёзно — мягко рекомендуй специалиста
- 200-400 слов
- В конце добавь планетарный мостик (мы все поддерживаем друг друга)"""),
            ("user", "{query}")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "age": age,
            "mood": mood,
            "target_lang": target_lang,
            "query": query
        })
        
        return response.content
    
    async def guided_meditation(self, duration: int = 5, focus: str = "calm", language: str = "ru") -> str:
        """Проводит медитацию на языке пользователя."""
        
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
            ("system", """Ты — мастер медитации One Planet Mentor.
Проведи медитацию длительностью {duration} минут с фокусом на {focus}.

ВАЖНО: Проводи медитацию СТРОГО на {target_lang} языке!

СТРУКТУРА:
1. Подготовка (1 минута)
2. Основная практика ({duration_minus_2} минут)
3. Завершение (1 минута)

Используй:
- Дыхательные техники
- Визуализацию
- Осознанность
- Мягкий, успокаивающий тон""")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "duration": duration,
            "focus": focus,
            "duration_minus_2": max(1, duration - 2),
            "target_lang": target_lang
        })
        
        return response.content
