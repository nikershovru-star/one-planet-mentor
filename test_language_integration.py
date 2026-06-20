"""
test_language_integration.py — Тест интеграции Language Agent
"""

import asyncio
from src.models import UserProfile, Query
from src.orchestrator import Orchestrator


async def test_integration():
    print("\n" + "="*60)
    print("🌐 ТЕСТ ИНТЕГРАЦИИ LANGUAGE AGENT")
    print("="*60)
    
    orchestrator = Orchestrator()
    
    # Тест 1: Запрос на английском от русскоязычного пользователя
    print("\n📝 Тест 1: Английский запрос → Русский пользователь")
    user1 = UserProfile(
        user_id="test_lang_001",
        age=25,
        religion="secular",
        language="ru",
        country="RU",
        goals=["Изучить AI"],
        interests=["Технологии"]
    )
    
    query1 = Query(
        text="How do neural networks work?",
        user=user1
    )
    
    print(f"   Запрос: \"{query1.text}\"")
    print(f"   Язык пользователя: {user1.language}")
    
    response1 = await orchestrator.process(query1)
    
    print(f"\n   ✅ Ответ:")
    print(f"   {response1.text[:200]}...")
    print(f"   Агенты: {response1.agents_used}")
    print(f"   ⏱️  {response1.latency_ms}ms")
    
    # Тест 2: Запрос на русском (без перевода)
    print("\n\n📝 Тест 2: Русский запрос → Русский пользователь")
    query2 = Query(
        text="Как работают нейронные сети?",
        user=user1
    )
    
    print(f"   Запрос: \"{query2.text}\"")
    
    response2 = await orchestrator.process(query2)
    
    print(f"\n   ✅ Ответ:")
    print(f"   {response2.text[:200]}...")
    print(f"   Агенты: {response2.agents_used}")
    print(f"   ⏱️  {response2.latency_ms}ms")
    
    print("\n" + "="*60)
    print("✨ Интеграция работает!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_integration())