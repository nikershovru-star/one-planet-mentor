"""
cache_manager.py — Кэширование ответов для ускорения
"""

import hashlib
import json
from cachetools import TTLCache
from typing import Optional


class ResponseCache:
    """Кэш ответов с TTL (time-to-live)."""
    
    def __init__(self, maxsize=1000, ttl=3600):
        """
        maxsize: максимальное количество записей
        ttl: время жизни кэша в секундах (1 час)
        """
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self.hits = 0
        self.misses = 0
    
    def _generate_key(self, query: str, age: int, language: str, religion: str) -> str:
        """Генерирует уникальный ключ для запроса."""
        key_data = f"{query}:{age}:{language}:{religion}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def get(self, query: str, age: int, language: str, religion: str) -> Optional[str]:
        """Получает ответ из кэша."""
        key = self._generate_key(query, age, language, religion)
        result = self.cache.get(key)
        if result:
            self.hits += 1
            print(f"   ⚡ Кэш-попадание! (hits: {self.hits}, misses: {self.misses})")
        else:
            self.misses += 1
        return result
    
    def set(self, query: str, age: int, language: str, religion: str, response: str):
        """Сохраняет ответ в кэш."""
        key = self._generate_key(query, age, language, religion)
        self.cache[key] = response
    
    def clear(self):
        """Очищает кэш."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> dict:
        """Возвращает статистику кэша."""
        return {
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0
        }


# Глобальный экземпляр кэша
response_cache = ResponseCache(maxsize=1000, ttl=3600)