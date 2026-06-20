"""
safety_agent.py — Агент безопасности.
Проверяет запросы на соответствие правилам (COPPA, GDPR, манифест).
"""

from .base_agent import BaseAgent
from ..models import SafetyCheck, AgentContext


class SafetyAgent(BaseAgent):
    """Проверяет безопасность запросов."""
    
    # Простые red flags для MVP
    RED_FLAGS = [
        "как сделать бомбу",
        "как взломать",
        "как убить",
        "как украсть",
        "как купить наркотики",
    ]
    
    def __init__(self):
        super().__init__("safety_agent")
    
    async def get_context(self, *args, **kwargs) -> AgentContext:
        """Заглушка — SafetyAgent не контекстный агент."""
        return AgentContext(
            agent_name="safety_agent",
            guidelines="",
            metadata={}
        )
    
    async def check(self, query: str, age: int) -> SafetyCheck:
        """Проверяет запрос на безопасность."""
        query_lower = query.lower()
        
        # Проверка на red flags
        for flag in self.RED_FLAGS:
            if flag in query_lower:
                return SafetyCheck(
                    is_safe=False,
                    reason="Potentially harmful content",
                    rejection_message="Извините, я не могу помочь с этим вопросом. Давайте поговорим о чём-то другом? 🌍"
                )
        
        # Возрастные ограничения
        if age < 13:
            # Дополнительная проверка для детей
            adult_flags = ["секс", "алкоголь", "насилие"]
            for flag in adult_flags:
                if flag in query_lower:
                    return SafetyCheck(
                        is_safe=False,
                        reason="Age-inappropriate content",
                        rejection_message="Этот вопрос не подходит для твоего возраста. Давай поговорим о чём-то интересном! 🌟"
                    )
        
        return SafetyCheck(is_safe=True)