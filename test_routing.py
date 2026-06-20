"""
test_routing.py — Тест правильного роутинга к экспертам
"""

import asyncio
from src.models import UserProfile, Query
from src.orchestrator import Orchestrator


async def test_routing():
    print("\n" + "="*70)
    print(" ТЕСТ ПРАВИЛЬНОГО РОУТИНГА")
    print("="*70)
    
    orchestrator = Orchestrator()
    
    user = UserProfile(
        user_id="routing_test_001",
        age=25,
        religion="secular",
        language="ru",
        country="RU",
        goals=["Изучить AI"],
        interests=["Технологии"]
    )
    
    tests = [
        ("Как работают нейронные сети?", "science_agent"),
        ("Как войти в IT в 25 лет?", "career_agent"),
        ("Напиши историю про космос", "creative_agent"),
        ("Как справиться с тревогой?", "wellness_agent"),
        ("Последние новости об AI", "search_agent"),
    ]
    
    for query_text, expected_agent in tests:
        print(f"\n{'='*70}")
        print(f"📝 Запрос: \"{query_text}\"")
        print(f"🎯 Ожидаемый эксперт: {expected_agent}")
        print(f"{'='*70}")
        
        query = Query(text=query_text, user=user)
        response = await orchestrator.process(query)
        
        print(f"\n✅ Ответ получен!")
        print(f"   Использованные агенты: {response.agents_used}")
        
        # Проверяем что нужный агент вызван
        expert_name = expected_agent.replace("_agent", "")
        if expert_name in response.agents_used:
            print(f"   ✅ {expected_agent} вызван!")
        else:
            print(f"   ⚠️  {expected_agent} НЕ вызван!")
        
        print(f"\n    Ответ: {response.text[:200]}...")
    
    print(f"\n{'='*70}")
    print("✨ Тест роутинга завершён!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    asyncio.run(test_routing())