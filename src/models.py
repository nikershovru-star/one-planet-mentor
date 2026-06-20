"""
models.py — Pydantic модели для One Planet Mentor
Определяют структуру данных пользователей и запросов.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class UserProfile(BaseModel):
    """Профиль пользователя — основа персонализации."""
    
    user_id: str = Field(..., description="Уникальный ID пользователя")
    age: int = Field(..., ge=5, le=99, description="Возраст 5-99")
    
    religion: Literal[
        "christian", "muslim", "jewish", 
        "buddhist", "hindu", "secular", "unspecified"
    ] = Field(default="unspecified", description="Религиозный контекст")
    
    language: str = Field(default="en", description="ISO 639-1 код языка")
    country: Optional[str] = Field(default=None, description="ISO 3166 код страны")
    
    goals: List[str] = Field(default_factory=list, description="Цели пользователя")
    interests: List[str] = Field(default_factory=list, description="Интересы")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Query(BaseModel):
    """Запрос пользователя."""
    
    text: str = Field(..., min_length=1, max_length=4000)
    user: UserProfile
    conversation_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentContext(BaseModel):
    """Контекст от контекстного агента."""
    
    agent_name: str
    guidelines: str
    metadata: dict = Field(default_factory=dict)


class SafetyCheck(BaseModel):
    """Результат проверки безопасности."""
    
    is_safe: bool
    reason: Optional[str] = None
    rejection_message: Optional[str] = None


class Response(BaseModel):
    """Финальный ответ пользователю."""
    
    text: str
    language: str
    age_group: str
    religion_context: str
    agents_used: List[str]
    tokens_used: int = 0
    latency_ms: int = 0


# Константы: возрастные группы
AGE_GROUPS = {
    (5, 8):   "toddlers",
    (9, 11):  "kids",
    (12, 14): "preteens",
    (15, 17): "teens",
    (18, 21): "students",
    (22, 25): "young_adults",
    (26, 30): "professionals",
    (31, 60): "mature",
    (61, 99): "elders",
}


def get_age_group(age: int) -> str:
    """Определяет возрастную группу по возрасту."""
    for (low, high), group in AGE_GROUPS.items():
        if low <= age <= high:
            return group
    return "mature"