"""
orchestrator.py — Главный AI-оркестратор
Координирует работу всех агентов, обеспечивает планетарную идеологию.
"""

import asyncio
import time
from typing import List

from .models import UserProfile, Query, Response, AgentContext, SafetyCheck
from .agents.age_agent import AgeAgent
from .agents.faith_agent import FaithAgent
from .agents.science_agent import ScienceAgent
from .agents.safety_agent import SafetyAgent


class Orchestrator:
    """
    Главный AI-оркестратор One Planet Mentor.
    
    Принцип работы:
    1. Safety Agent проверяет запрос
    2. Контекстные агенты работают параллельно (Age, Faith, Language...)
    3. Экспертный агент генерирует ответ
    4. Orchestrator собирает финальный ответ
    5. Проверка соответствия планетарному манифесту
    """
    
    PLANETARY_VALUES = [
        "забота о планете",
        "доброта и милосердие",
        "единство в различии",
        "стремление к знанию",
        "справедливость",
    ]
    
    def __init__(self):
        self.age_agent = AgeAgent()
        self.faith_agent = FaithAgent()
        self.science_agent = ScienceAgent()
        self.safety_agent = SafetyAgent()
    
    async def process(self, query: Query) -> Response:
        """Главный метод обработки запроса."""
        start_time = time.time()
        
        # Шаг 1: Проверка безопасности
        safety = await self.safety_agent.check(query.text, query.user.age)
        if not safety.is_safe:
            return Response(
                text=safety.rejection_message or "Извините, не могу ответить.",
                language=query.user.language,
                age_group="unknown",
                religion_context="unknown",
                agents_used=["safety"]
            )
        
        # Шаг 2: Параллельный вызов контекстных агентов
        age_ctx, faith_ctx = await asyncio.gather(
            self.age_agent.get_context(query.user.age, query.text),
            self.faith_agent.get_context(query.user.religion, query.text)
        )
        
        # Шаг 3: Экспертный ответ
        expert_response = await self.science_agent.answer(
            query=query.text,
            age_context=age_ctx,
            faith_context=faith_ctx
        )
        
        # Шаг 4: Финальная сборка
        final_text = self._synthesize(expert_response, age_ctx, faith_ctx)
        
        # Шаг 5: Проверка планетарного манифеста
        if not self._aligns_with_manifest(final_text):
            final_text = self._add_planetary_bridge(final_text, query.user.religion)
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        return Response(
            text=final_text,
            language=query.user.language,
            age_group=age_ctx.metadata.get("group", "unknown"),
            religion_context=faith_ctx.metadata.get("religion", "unknown"),
            agents_used=["safety", "age", "faith", "science", "orchestrator"],
            latency_ms=latency_ms
        )
    
    def _synthesize(self, expert: str, age_ctx: AgentContext, faith_ctx: AgentContext) -> str:
        """Собирает финальный ответ из частей."""
        # В MVP — просто возвращаем ответ эксперта.
        # В полной версии — LLM-синтез с учётом всех контекстов.
        return expert
    
    def _aligns_with_manifest(self, text: str) -> bool:
        """Проверяет, не противоречит ли ответ планетарному единству."""
        red_flags = [
            "наша вера лучше", "наша религия истинная",
            "неверные", "только мы", "они ошибаются"
        ]
        text_lower = text.lower()
        return not any(flag in text_lower for flag in red_flags)
    
    def _add_planetary_bridge(self, text: str, religion: str) -> str:
        """Добавляет мостик к планетарному единству."""
        bridges = {
            "christian": "\n\n💙 Эта ценность объединяет всех людей планеты.",
            "muslim":    "\n\n Это объединяет нас всех на одной Земле.",
            "jewish":    "\n\n✨ Тикун олам — исправление мира для всех.",
            "buddhist":  "\n\n️ Мы все взаимосвязаны на этой планете.",
            "hindu":     "\n\n️ Васудхайва кутумбакам — весь мир одна семья.",
            "secular":   "\n\n🌱 Общая ценность всего человечества.",
        }
        return text + bridges.get(religion, "\n\n🌍 Мы все — одна семья на планете.")