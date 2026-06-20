"""
age_agent.py — Агент адаптации под возраст.
Использует локальную Ollama (llama3:latest).
"""

import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from .base_agent import BaseAgent
from ..models import AgentContext, get_age_group


class AgeAgent(BaseAgent):
    """Адаптирует контент под возраст пользователя."""
    
    def __init__(self):
        super().__init__("age_agent")
        model = os.getenv("AGE_AGENT_MODEL", "llama3:latest")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.3
        )
    
    async def get_context(self, age: int, query: str) -> AgentContext:
        group = get_age_group(age)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — эксперт по возрастной психологии.
Группа пользователя: {group} (возраст {age}).

Дай КРАТКИЕ рекомендации (3-4 пункта) по:
1. Стиль языка (сложность, длина)
2. Темы и примеры, которые зацепят
3. Тон общения
4. Чего избегать

Отвечай на РУССКОМ языке. Будь конкретным."""),
            ("user", "Запрос пользователя: {query}")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "group": group, "age": age, "query": query
        })
        
        return AgentContext(
            agent_name="age_agent",
            guidelines=response.content,
            metadata={"group": group, "age": age}
        )