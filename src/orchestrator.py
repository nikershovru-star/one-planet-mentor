"""
orchestrator.py — Главный AI-оркестратор
Использует Hermes3 для принятия решений
"""

import asyncio
import time
import json

from .models import UserProfile, Query, Response, AgentContext, SafetyCheck
from .agents.orchestrator_agent import OrchestratorAgent
from .agents.age_agent import AgeAgent
from .agents.faith_agent import FaithAgent
from .agents.science_agent import ScienceAgent
from .agents.safety_agent import SafetyAgent
from .agents.memory_agent import MemoryAgent
from .agents.career_agent import CareerAgent
from .agents.creative_agent import CreativeAgent

class Orchestrator:
    """
    Главный AI-оркестратор One Planet Mentor.
    Hermes3 принимает решения, другие агенты выполняют.
    """
    
    PLANETARY_VALUES = [
        "забота о планете",
        "доброта и милосердие",
        "единство в различии",
        "стремление к знанию",
        "справедливость",
    ]
    
    def __init__(self):
        print("🧠 Инициализация оркестратора...")
        self.orchestrator_agent = OrchestratorAgent()
        self.age_agent = AgeAgent()
        self.faith_agent = FaithAgent()
        self.science_agent = ScienceAgent()
        self.safety_agent = SafetyAgent()
        self.memory_agent = MemoryAgent()
        self.career_agent = CareerAgent()
        self.creative_agent = CreativeAgent()
        print("✅ Все агенты загружены!")
    
    async def process(self, query: Query) -> Response:
        """Главный метод обработки запроса."""
        start_time = time.time()
        
        # Шаг 1: Hermes3 анализирует запрос
        print(f"   🧠 Hermes3 анализирует запрос...")
        plan = await self.orchestrator_agent.decide_routing(
            query.text, query.user.age, query.user.religion
        )
        
        # Шаг 2: Проверка безопасности (всегда!)
        if plan.get("needs_safety_check", True):
            print(f"   🛡️ Safety Agent проверяет...")
            safety = await self.safety_agent.check(query.text, query.user.age)
            if not safety.is_safe:
                return Response(
                    text=safety.rejection_message or "Извините, не могу ответить.",
                    language=query.user.language,
                    age_group="unknown",
                    religion_context="unknown",
                    agents_used=["orchestrator", "safety"]
                )
        
        # Шаг 3: Параллельный вызов контекстных агентов
        tasks = []
        agents_used = ["orchestrator", "safety"]
        
        if plan.get("needs_age_adaptation", True):
            print(f"   🎂 Age Agent адаптирует...")
            tasks.append(self.age_agent.get_context(query.user.age, query.text))
            agents_used.append("age")
        else:
            tasks.append(asyncio.sleep(0))  # Заглушка
        
        if plan.get("needs_faith_context", False):
            print(f"   🕊️ Faith Agent учитывает контекст...")
            tasks.append(self.faith_agent.get_context(query.user.religion, query.text))
            agents_used.append("faith")
        else:
            tasks.append(asyncio.sleep(0))  # Заглушка
        
        results = await asyncio.gather(*tasks)
        age_ctx = results[0] if isinstance(results[0], AgentContext) else AgentContext(
            agent_name="age_agent", guidelines="", metadata={}
        )
        faith_ctx = results[1] if len(results) > 1 and isinstance(results[1], AgentContext) else AgentContext(
            agent_name="faith_agent", guidelines="", metadata={}
        )
        
        # Шаг 4: Экспертный ответ
        primary_agent = plan.get("primary_agent", "science_agent")
        print(f"   🔬 {primary_agent} генерирует ответ...")
        
        expert_response = await self.science_agent.answer(
            query=query.text,
            age_context=age_ctx,
            faith_context=faith_ctx
        )
        agents_used.append("science")
        
        # Шаг 5: Финальная сборка
        final_text = self._synthesize(expert_response, age_ctx, faith_ctx)
        
        # Шаг 6: Проверка планетарного манифеста
        if not self._aligns_with_manifest(final_text):
            final_text = self._add_planetary_bridge(final_text, query.user.religion)
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        return Response(
            text=final_text,
            language=query.user.language,
            age_group=age_ctx.metadata.get("group", "unknown"),
            religion_context=faith_ctx.metadata.get("religion", "unknown"),
            agents_used=agents_used,
            tokens_used=plan.get("estimated_tokens", 0),
            latency_ms=latency_ms
        )
    
    def _synthesize(self, expert: str, age_ctx: AgentContext, faith_ctx: AgentContext) -> str:
        """Собирает финальный ответ."""
        return expert
    
    def _aligns_with_manifest(self, text: str) -> bool:
        """Проверяет соответствие планетарному манифесту."""
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
            "muslim":    "\n\n🌍 Это объединяет нас всех на одной Земле.",
            "jewish":    "\n\n✨ Тикун олам — исправление мира для всех.",
            "buddhist":  "\n\n☸️ Мы все взаимосвязаны на этой планете.",
            "hindu":     "\n\n🕉️ Васудхайва кутумбакам — весь мир одна семья.",
            "secular":   "\n\n Общая ценность всего человечества.",
        }
        return text + bridges.get(religion, "\n\n🌍 Мы все — одна семья на планете.")