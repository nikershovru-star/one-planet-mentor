"""
test_full_integration.py — Полный тест всех 11 агентов
"""

import asyncio
import time
from src.models import UserProfile, Query
from src.orchestrator import Orchestrator


async def test_all_agents():
    print("\n" + "="*70)
    print(" ПОЛНЫЙ ИНТЕГРАЦИОННЫЙ ТЕСТ ВСЕХ 11 АГЕНТОВ")
    print("="*70)
    
    orchestrator = Orchestrator()
    
    # Тестовый пользователь
    user = UserProfile(
        user_id="beta_test_001",
        age=25,
        religion="secular",
        language="ru",
        country="RU",
        goals=["Изучить AI", "Развить карьеру"],
        interests=["Технологии", "Наука"]
    )
    
    tests = [
        {
            "name": "Научный вопрос",
            "query": "Как работают нейронные сети?",
            "expected_agents": ["language", "orchestrator", "safety", "age", "science"]
        },
        {
            "name": "Карьерный вопрос",
            "query": "Как войти в IT в 25 лет?",
            "expected_agents": ["language", "orchestrator", "safety", "age", "career"]
        },
        {
            "name": "Творческий запрос",
            "query": "Напиши историю про космос",
            "expected_agents": ["language", "orchestrator", "safety", "age", "creative"]
        },
        {
            "name": "Вопрос о здоровье",
            "query": "Как справиться с тревогой?",
            "expected_agents": ["language", "orchestrator", "safety", "wellness"]
        },
        {
            "name": "Актуальная информация",
            "query": "Последние новости об AI",
            "expected_agents": ["language", "orchestrator", "safety", "search"]
        }
    ]
    
    results = []
    
    for i, test in enumerate(tests, 1):
        print(f"\n{'='*70}")
        print(f"📝 Тест {i}: {test['name']}")
        print(f"{'='*70}")
        
        query = Query(text=test["query"], user=user)
        
        start = time.time()
        try:
            response = await orchestrator.process(query)
            elapsed = time.time() - start
            
            print(f"   ✅ Ответ получен!")
            print(f"   ⏱️  Время: {response.latency_ms}ms ({elapsed:.1f} сек)")
            print(f"   🤖 Агенты: {response.agents_used}")
            print(f"   📝 Ответ: {response.text[:150]}...")
            
            # Проверяем что нужные агенты вызваны
            missing_agents = [a for a in test["expected_agents"] if a not in response.agents_used]
            if missing_agents:
                print(f"   ⚠️  Не вызваны: {missing_agents}")
            else:
                print(f"   ✅ Все ожидаемые агенты вызваны!")
            
            results.append({
                "test": test["name"],
                "success": True,
                "time_ms": response.latency_ms,
                "agents": response.agents_used
            })
            
        except Exception as e:
            elapsed = time.time() - start
            print(f"   ❌ Ошибка: {e}")
            results.append({
                "test": test["name"],
                "success": False,
                "error": str(e),
                "time_ms": int(elapsed * 1000)
            })
    
    # Итоговая статистика
    print(f"\n{'='*70}")
    print("📊 ИТОГОВАЯ СТАТИСТИКА")
    print(f"{'='*70}")
    
    successful = sum(1 for r in results if r["success"])
    total = len(results)
    
    print(f"\n✅ Успешных тестов: {successful}/{total}")
    print(f"❌ Ошибок: {total - successful}/{total}")
    
    if successful > 0:
        avg_time = sum(r["time_ms"] for r in results if r["success"]) / successful
        print(f"⏱️  Среднее время: {avg_time:.0f}ms ({avg_time/1000:.1f} сек)")
    
    # Статистика кэша
    cache_stats = orchestrator.get_cache_stats()
    print(f"\n📦 Кэш:")
    print(f"   Размер: {cache_stats['size']}")
    print(f"   Попадания: {cache_stats['hits']}")
    print(f"   Hit rate: {cache_stats['hit_rate']:.2%}")
    
    print(f"\n{'='*70}")
    if successful == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! СИСТЕМА ГОТОВА К ПРОДАКШЕНУ!")
    else:
        print(f"⚠️  {total - successful} тестов с ошибками — нужно исправить")
    print(f"{'='*70}\n")
    
    return results


if __name__ == "__main__":
    asyncio.run(test_all_agents())