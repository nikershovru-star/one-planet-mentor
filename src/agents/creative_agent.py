"""
creative_agent.py — Творческий агент
Генерирует идеи, истории, стихи, творческие задания
Учитывает язык пользователя
"""

import os
import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from .base_agent import BaseAgent
from ..models import AgentContext


class CreativeAgent(BaseAgent):
    """Генерирует творческий контент: истории, идеи, стихи, задания."""
    
    def __init__(self):
        super().__init__("creative_agent")
        model = os.getenv("CREATIVE_AGENT_MODEL", "llama3:latest")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.8
        )
    
    async def get_context(self, age: int, query: str) -> AgentContext:
        """Определяет тип творческого запроса."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — классификатор творческих запросов.
Определи тип запроса и дай рекомендации по стилю.

Типы: story|poem|idea|art_prompt|music|game|other

Формат (JSON):
{{
  "type": "story",
  "mood": "вдохновляющий",
  "complexity": "medium",
  "style_tips": ["совет1", "совет2"]
}}

Отвечай ТОЛЬКО JSON."""),
            ("user", "Возраст: {age}\nЗапрос: {query}")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({"age": age, "query": query})
        
        try:
            text = response.content.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            creative_data = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            creative_data = {
                "type": "other",
                "mood": "neutral",
                "complexity": "medium",
                "style_tips": []
            }
        
        return AgentContext(
            agent_name="creative_agent",
            guidelines=json.dumps(creative_data, ensure_ascii=False),
            metadata=creative_data
        )
    
    async def create(self, query: str, age: int, creative_type: str = "story", language: str = "ru") -> str:
        """Генерирует творческий контент на языке пользователя."""
        
        type_prompts = {
            "story": "Напиши интересную историю",
            "poem": "Напиши стихотворение",
            "idea": "Предложи 5 креативных идей",
            "art_prompt": "Опиши идею для картины",
            "music": "Предложи музыкальную идею",
            "game": "Придумай игру",
            "other": "Ответь творчески"
        }
        
        instruction = type_prompts.get(creative_type, "Ответь творчески")
        
        # Маппинг языков
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
            ("system", """Ты — творческий наставник One Planet Mentor.
{instruction} для пользователя возраста {age}.

ВАЖНО: Отвечай СТРОГО на {target_lang} языке!

ПРАВИЛА:
- Будь оригинальным и вдохновляющим
- Адаптируй сложность под возраст
- Используй яркие образы и метафоры
- В конце добавь планетарный мостик (как это объединяет людей)
- 150-300 слов"""),
            ("user", "{query}")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "instruction": instruction,
            "age": age,
            "target_lang": target_lang,
            "query": query
        })
        
        return response.content
