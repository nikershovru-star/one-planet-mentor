"""
test_orchestrator.py — Тест оркестратора на Hermes3
"""

import asyncio
from src.models import UserProfile, Query
from src.orchestrator import Orchestrator


async def test_orchestrator():
    print("\n" + "="*60)
    print("🧠 ТЕСТ ОРКЕСТРАТОРА НА HERMES3")
    print("="*60)
    
    orchestrator = Orchestrator()
    
    # Тестовый пользователь
    user = UserProfile(
        user_id="test_hermes_001",
        age=25,
        religion="secular",
        language="ru",
        country="RU",
        goals=["Изучить AI"],
        interests=["Технологии"]
    )
    
    # Тестовый запрос
    query = Query(
        text="Как работают нейронные сети?",
        user=user
    )
    
    print(f"\n📝 Запрос: \"{query.text}\"")
    print(f"👤 Пользователь: {user.age} лет, {user.religion}")
    
    print(f"\n⏳ Обрабатываем запрос...")
    response = await orchestrator.process(query)
    
    print(f"\n✅ Ответ получен!")
    print(f"    Текст: {response.text[:200]}...")
    print(f"    Агенты: {response.agents_used}")
    print(f"   ⏱️  Время: {response.latency_ms}ms")
    
    print("\n" + "="*60)
    print("✨ Тест завершён!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_orchestrator())