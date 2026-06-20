"""
science_agent.py — Экспертный агент по науке.
Использует локальную Ollama (qwen3:14b).
"""

import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from .base_agent import BaseAgent
from ..models import AgentContext


class ScienceAgent(BaseAgent):
    """Отвечает на научные вопросы с учётом контекста."""
    
    def __init__(self):
        super().__init__("science_agent")
        model = os.getenv("SCIENCE_AGENT_MODEL", "qwen3:14b")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.4
        )
    async def get_context(self, *args, **kwargs) -> AgentContext:
        """Заглушка — ScienceAgent не контекстный агент."""
        return AgentContext(
            agent_name="science_agent",
            guidelines="",
            metadata={}
        )
    
    async def answer(
        self, 
        query: str, 
        age_context: AgentContext, 
        faith_context: AgentContext
    ) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — дружелюбный учёный-наставник One Planet Mentor.

🎯 ТВОЯ МИССИЯ:
Объяснять науку так, чтобы это объединяло людей планеты,
а не разделяло их.

📚 ВОЗРАСТНОЙ КОНТЕКСТ (адаптируй ответ):
{age_guidelines}

🕊️ РЕЛИГИОЗНЫЙ КОНТЕКСТ (вторичный! уважай, но не доминируй):
{faith_guidelines}

🌍 ПЛАНЕТАРНЫЙ МОСТ (подчеркни в конце):
{planetary_bridge}

📝 ПРАВИЛА:
- Отвечай на том же языке, что и запрос
- Будь точным в фактах
- Используй примеры и аналогии
- В конце добавь планетарный мостик (1 предложение)
- НЕ проповедуй, НЕ навязывай
- Будь тёплым и дружелюбным

Дай развёрнутый, но не слишком длинный ответ (150-300 слов)."""),
            ("user", "{query}")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "age_guidelines": age_context.guidelines,
            "faith_guidelines": faith_context.guidelines,
            "planetary_bridge": faith_context.metadata.get("planetary_bridge", ""),
            "query": query
        })
        
        return response.content