"""
orchestrator.py — Оптимизированный AI-оркестратор
Параллельные вызовы агентов + кэширование + интеграция всех 11 агентов
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
from .agents.language_agent import LanguageAgent
from .agents.wellness_agent import WellnessAgent
from .agents.search_agent import SearchAgent
from .cache_manager import response_cache
from .config import get_config, get_cached_translation, cache_translation


class Orchestrator:
    """
    Оптимизированный AI-оркестратор One Planet Mentor.
    Все 11 агентов работают параллельно когда возможно.
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
        config = get_config()
        print(f"   Режим: {config['description']}")
        
        # Все агенты
        self.orchestrator_agent = OrchestratorAgent()
        self.age_agent = AgeAgent()
        self.faith_agent = FaithAgent()
        self.science_agent = ScienceAgent()
        self.safety_agent = SafetyAgent()
        self.memory_agent = MemoryAgent()
        self.career_agent = CareerAgent()
        self.creative_agent = CreativeAgent()
        self.language_agent = LanguageAgent()
        self.wellness_agent = WellnessAgent()
        self.search_agent = SearchAgent()
        
        self.config = config
        print("✅ Все 11 агентов загружены!")
    
    async def process(self, query: Query) -> Response:
        """Главный метод обработки запроса с оптимизацией."""
        start_time = time.time()
        agents_used = []
        
        # Шаг 1: Проверяем кэш ответов
        cached_response = response_cache.get(
            query.text, query.user.age, query.user.language, query.user.religion
        )
        
        if cached_response:
            return Response(
                text=cached_response,
                language=query.user.language,
                age_group="unknown",
                religion_context="unknown",
                agents_used=["cache"],
                latency_ms=int((time.time() - start_time) * 1000)
            )
        
        # Шаг 2: Language Agent (если включён)
        working_query = query.text
        detected_lang = query.user.language
        needs_back_translation = False
        
        if self.config["use_language_agent"]:
            print(f"    Language Agent...")
            lang_context = await self.language_agent.get_context(query.text, query.user.language)
            detected_lang = lang_context.metadata.get("detected_language", query.user.language)
            needs_translation = lang_context.metadata.get("needs_translation", False)
            agents_used.append("language")
            
            if needs_translation and detected_lang != query.user.language:
                # Проверяем кэш переводов
                cached = get_cached_translation(query.text, detected_lang, query.user.language)
                if cached:
                    print(f"   ⚡ Перевод из кэша!")
                    working_query = cached
                else:
                    print(f"   🔄 Переводим запрос...")
                    working_query = await self.language_agent.translate(
                        query.text, detected_lang, query.user.language
                    )
                    cache_translation(query.text, detected_lang, query.user.language, working_query)
                needs_back_translation = True
        
        # Шаг 3: Hermes3 анализирует запрос (если включён)
        plan = {}
        if self.config["use_orchestrator"]:
            print(f"    Hermes3 анализирует...")
            plan = await self.orchestrator_agent.decide_routing(
                working_query, query.user.age, query.user.religion, query.user.language
            )
            agents_used.append("orchestrator")
        else:
            # Быстрый режим — стандартный план
            plan = {
                "needs_safety_check": True,
                "needs_age_adaptation": True,
                "needs_faith_context": query.user.religion != "unspecified",
                "needs_search": False,
                "needs_wellness": False,
                "primary_agent": "science_agent"
            }
        
        # Шаг 4: Safety Agent (всегда!)
        print(f"   🛡️ Safety Agent...")
        safety = await self.safety_agent.check(working_query, query.user.age)
        agents_used.append("safety")
        
        if not safety.is_safe:
            return Response(
                text=safety.rejection_message or "Извините, не могу ответить.",
                language=query.user.language,
                age_group="unknown",
                religion_context="unknown",
                agents_used=agents_used
            )
        
        # Шаг 5: ПАРАЛЛЕЛЬНЫЙ запуск всех контекстных агентов
        print(f"   ⚡ Параллельный запуск агентов...")
        
        tasks = []
        task_names = []
        
        # Age Agent
        if plan.get("needs_age_adaptation", True):
            tasks.append(self.age_agent.get_context(query.user.age, working_query))
            task_names.append("age")
        
        # Faith Agent
        if plan.get("needs_faith_context", False):
            tasks.append(self.faith_agent.get_context(query.user.religion, working_query))
            task_names.append("faith")
        
        # Memory Agent
        if self.config["use_memory_agent"] and plan.get("needs_memory", True):
            tasks.append(self.memory_agent.get_context(query.user.user_id, working_query))
            task_names.append("memory")
        
        # Search Agent
        if self.config["use_search_agent"] and plan.get("needs_search", False):
            search_type = plan.get("search_type", "web")
            tasks.append(self.search_agent.get_context(working_query, search_type))
            task_names.append("search")
        
        # Wellness Agent
        if self.config["use_wellness_agent"] and plan.get("needs_wellness", False):
            tasks.append(self.wellness_agent.get_context(query.user.age, working_query))
            task_names.append("wellness")
        
        # Запускаем все параллельно
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            contexts = {}
            for name, result in zip(task_names, results):
                if isinstance(result, AgentContext):
                    contexts[name] = result
                    agents_used.append(name)
                elif isinstance(result, Exception):
                    print(f"   ⚠️  Ошибка {name}: {result}")
        else:
            contexts = {}
        
        # Шаг 6: Экспертный ответ
        primary_agent = plan.get("primary_agent", "science_agent")
        print(f"   🔬 {primary_agent} генерирует ответ...")
        
        expert_response = await self.science_agent.answer(
            query=working_query,
            age_context=contexts.get("age", AgentContext(agent_name="age_agent", guidelines="", metadata={})),
            faith_context=contexts.get("faith", AgentContext(agent_name="faith_agent", guidelines="", metadata={}))
        )
        agents_used.append("science")
        
        # Шаг 7: Перевод обратно (если был перевод)
        final_text = expert_response
        if needs_back_translation:
            cached_back = get_cached_translation(expert_response, query.user.language, detected_lang)
            if cached_back:
                print(f"   ⚡ Обратный перевод из кэша!")
                final_text = cached_back
            else:
                print(f"    Обратный перевод...")
                final_text = await self.language_agent.translate(
                    expert_response, query.user.language, detected_lang
                )
                cache_translation(expert_response, query.user.language, detected_lang, final_text)
        
        # Шаг 8: Финальная сборка
        final_text = self._synthesize(final_text, contexts)
        
        # Шаг 9: Проверка планетарного манифеста
        if not self._aligns_with_manifest(final_text):
            final_text = self._add_planetary_bridge(final_text, query.user.religion)
        
        # Шаг 10: Сохраняем в кэш
        response_cache.set(
            query.text, query.user.age, query.user.language, query.user.religion, final_text
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        return Response(
            text=final_text,
            language=query.user.language,
            age_group=contexts.get("age", AgentContext(agent_name="", guidelines="", metadata={})).metadata.get("group", "unknown"),
            religion_context=contexts.get("faith", AgentContext(agent_name="", guidelines="", metadata={})).metadata.get("religion", "unknown"),
            agents_used=agents_used,
            tokens_used=plan.get("estimated_tokens", 0),
            latency_ms=latency_ms
        )
    
    def _synthesize(self, expert: str, contexts: dict) -> str:
        """Собирает финальный ответ с учётом всех контекстов."""
        return expert
    
    def _aligns_with_manifest(self, text: str) -> bool:
        """Проверяет соответствие планетарному манифесту."""
        red_flags = ["наша вера лучше", "наша религия истинная", "неверные", "только мы"]
        text_lower = text.lower()
        return not any(flag in text_lower for flag in red_flags)
    
    def _add_planetary_bridge(self, text: str, religion: str) -> str:
        """Добавляет мостик к планетарному единству."""
        bridges = {
            "christian": "\n\n💙 Эта ценность объединяет всех людей планеты.",
            "muslim": "\n\n🌍 Это объединяет нас всех на одной Земле.",
            "jewish": "\n\n✨ Тикун олам — исправление мира для всех.",
            "buddhist": "\n\n☸️ Мы все взаимосвязаны на этой планете.",
            "hindu": "\n\n🕉️ Васудхайва кутумбакам — весь мир одна семья.",
            "secular": "\n\n Общая ценность всего человечества.",
        }
        return text + bridges.get(religion, "\n\n Мы все — одна семья на планете.")
    
    def get_cache_stats(self) -> dict:
        """Возвращает статистику кэша."""
        return response_cache.get_stats()