"""
test_optimization.py — Тест оптимизации и интеграции
"""

import asyncio
import time
from src.models import UserProfile, Query
from src.orchestrator import Orchestrator


async def test_optimization():
    print("\n" + "="*60)
    print("⚡ ТЕСТ ОПТИМИЗАЦИИ + ИНТЕГРАЦИИ")
    print("="*60)
    
    orchestrator = Orchestrator()
    
    user = UserProfile(
        user_id="test_opt_001",
        age=25,
        religion="secular",
        language="ru",
        country="RU",
        goals=["Изучить AI"],
        interests=["Технологии"]
    )
    
    # Тест 1: Первый запрос (без кэша)
    print("\n📝 Тест 1: Первый запрос")
    query1 = Query(text="Как работают нейронные сети?", user=user)
    
    start = time.time()
    response1 = await orchestrator.process(query1)
    time1 = time.time() - start
    
    print(f"   ⏱️  Время: {response1.latency_ms}ms ({time1:.1f} сек)")
    print(f"   Агенты: {response1.agents_used}")
    print(f"   Ответ: {response1.text[:100]}...")
    
    # Тест 2: Тот же запрос (из кэша)
    print("\n\n📝 Тест 2: Тот же запрос (кэш)")
    query2 = Query(text="Как работают нейронные сети?", user=user)
    
    start = time.time()
    response2 = await orchestrator.process(query2)
    time2 = time.time() - start
    
    print(f"   ️  Время: {response2.latency_ms}ms ({time2:.3f} сек)")
    print(f"   Агенты: {response2.agents_used}")
    
    # Тест 3: Другой запрос
    print("\n\n📝 Тест 3: Другой запрос")
    query3 = Query(text="Что такое гравитация?", user=user)
    
    start = time.time()
    response3 = await orchestrator.process(query3)
    time3 = time.time() - start
    
    print(f"   ⏱️  Время: {response3.latency_ms}ms ({time3:.1f} сек)")
    print(f"   Агенты: {response3.agents_used}")
    
    # Статистика
    print("\n\n Статистика кэша:")
    stats = orchestrator.get_cache_stats()
    print(f"   Размер: {stats['size']}")
    print(f"   Попадания: {stats['hits']}")
    print(f"   Промахи: {stats['misses']}")
    print(f"   Hit rate: {stats['hit_rate']:.2%}")
    
    print("\n" + "="*60)
    if time2 > 0.001:
        print(f"✨ Ускорение: {time1/time2:.0f}x при повторном запросе!")
    else:
        print(f"✨ Кэш сработал мгновенно! (< 1ms)")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_optimization())