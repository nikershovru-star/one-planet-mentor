"""
config.py — Конфигурация системы
Управление агентами, кэшем, оптимизацией
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Режим работы: "fast" | "balanced" | "quality"
MODE = os.getenv("MODE", "balanced")

# Настройки для каждого режима
MODE_CONFIGS = {
    "fast": {
        "use_orchestrator": False,
        "use_language_agent": False,
        "use_search_agent": False,
        "use_wellness_agent": False,
        "use_memory_agent": False,
        "parallel_context_agents": True,
        "max_agents": 3,
        "description": "Быстрый режим — только основные агенты"
    },
    "balanced": {
        "use_orchestrator": True,
        "use_language_agent": True,
        "use_search_agent": True,
        "use_wellness_agent": False,
        "use_memory_agent": True,
        "parallel_context_agents": True,
        "max_agents": 6,
        "description": "Баланс скорости и качества"
    },
    "quality": {
        "use_orchestrator": True,
        "use_language_agent": True,
        "use_search_agent": True,
        "use_wellness_agent": True,
        "use_memory_agent": True,
        "parallel_context_agents": True,
        "max_agents": 11,
        "description": "Максимальное качество — все агенты"
    }
}

def get_config():
    """Возвращает текущую конфигурацию."""
    return MODE_CONFIGS.get(MODE, MODE_CONFIGS["balanced"])

# Кэш переводов (отдельный от кэша ответов)
TRANSLATION_CACHE = {}

def get_cached_translation(text: str, from_lang: str, to_lang: str) -> str | None:
    """Получает перевод из кэша."""
    key = f"{text}:{from_lang}:{to_lang}"
    return TRANSLATION_CACHE.get(key)

def cache_translation(text: str, from_lang: str, to_lang: str, translation: str):
    """Сохраняет перевод в кэш."""
    key = f"{text}:{from_lang}:{to_lang}"
    TRANSLATION_CACHE[key] = translation
    # Ограничиваем размер кэша
    if len(TRANSLATION_CACHE) > 500:
        # Удаляем половину старых записей
        keys = list(TRANSLATION_CACHE.keys())[:250]
        for k in keys:
            del TRANSLATION_CACHE[k]