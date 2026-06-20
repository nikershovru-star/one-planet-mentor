"""
faith_agent.py — Агент религиозного контекста.
Использует локальную Ollama (qwen3:14b).
Планетарная идентичность первична.
"""

import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from .base_agent import BaseAgent
from ..models import AgentContext


class FaithAgent(BaseAgent):
    """Учитывает религиозный контекст, сохраняя планетарное единство."""
    
    PLANETARY_BRIDGES = {
        "christian": "Возлюби ближнего → забота о всех людях планеты",
        "muslim":    "Умма → братство 8 млрд жителей Земли",
        "jewish":    "Тикун олам → исправление мира для всех",
        "buddhist":  "Взаимозависимость → единство всего живого",
        "hindu":     "Васудхайва кутумбакам → весь мир одна семья",
        "secular":   "Гуманизм → ценность каждого человека",
        "unspecified": "Универсальные человеческие ценности",
    }
    
    def __init__(self):
        super().__init__("faith_agent")
        model = os.getenv("FAITH_AGENT_MODEL", "qwen3:14b")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.3
        )
    
    async def get_context(self, religion: str, query: str) -> AgentContext:
        bridge = self.PLANETARY_BRIDGES.get(religion, "")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — эксперт по межконфессиональному диалогу.

КРИТИЧЕСКИЕ ПРИНЦИПЫ:
1. Планетарная идентичность ПЕРВИЧНА, религиозная — вторична
2. НИКОГДА не ставь одну религию выше другой
3. Подчёркивай ОБЩИЕ ценности всех традиций
4. НЕ критикуй другие верования
5. Цитаты — только если релевантны и с контекстом

Традиция пользователя: {religion}
Мост к планетарным ценностям: {bridge}

Дай 3-4 краткие рекомендации на РУССКОМ, как учесть традицию,
сохраняя единство всех жителей планеты."""),
            ("user", "Запрос: {query}")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "religion": religion,
            "bridge": bridge,
            "query": query
        })
        
        return AgentContext(
            agent_name="faith_agent",
            guidelines=response.content,
            metadata={
                "religion": religion,
                "planetary_bridge": bridge
            }
        )