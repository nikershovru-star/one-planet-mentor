"""
base_agent.py — Базовый класс для всех AI-агентов.
Все агенты наследуются от этого класса.
"""

from abc import ABC, abstractmethod
from ..models import AgentContext


class BaseAgent(ABC):
    """Абстрактный базовый класс для всех агентов."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def get_context(self, *args, **kwargs) -> AgentContext:
        """Возвращает контекст для экспертного агента."""
        pass