"""
test_wellness.py — Тест Wellness Agent
"""

import asyncio
from src.agents.wellness_agent import WellnessAgent


async def test_wellness():
    print("\n" + "="*60)
    print("💚 ТЕСТ WELLNESS AGENT")
    print("="*60)
    
    agent = WellnessAgent()
    
    # Тест 1: Анализ настроения
    print("\n🔍 1. АНАЛИЗ НАСТРОЕНИЯ")
    ctx = await agent.get_context(25, "Я чувствую тревогу перед экзаменом", "anxious")
    print(f"   Настроение: {ctx.metadata.get('mood_detected')}")
    print(f"   Серьёзность: {ctx.metadata.get('severity')}")
    print(f"   Рекомендации: {ctx.metadata.get('recommendations')}")
    
    # Тест 2: Поддержка
    print("\n💙 2. ПОДДЕРЖКА")
    support = await agent.provide_support(
        "Я чувствую тревогу перед экзаменом",
        25,
        "anxious"
    )
    print(f"   {support[:200]}...")
    
    # Тест 3: Медитация
    print("\n 3. МЕДИТАЦИЯ")
    meditation = await agent.guided_meditation(5, "calm")
    print(f"   {meditation[:200]}...")
    
    print("\n" + "="*60)
    print("✨ Wellness Agent работает!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_wellness())