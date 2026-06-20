"""
test_new_agents.py — Тест новых агентов
"""

import asyncio
from src.agents.memory_agent import MemoryAgent
from src.agents.career_agent import CareerAgent
from src.agents.creative_agent import CreativeAgent


async def test_agents():
    print("\n" + "="*60)
    print("🧠 ТЕСТ НОВЫХ АГЕНТОВ")
    print("="*60)
    
    # Memory Agent
    print("\n📚 1. MEMORY AGENT")
    memory = MemoryAgent()
    ctx = await memory.get_context("test_user_123", "Как работают нейросети?")
    print(f"   Контекст: {ctx.guidelines[:100]}...")
    print(f"   Метаданные: {ctx.metadata}")
    
    # Career Agent
    print("\n💼 2. CAREER AGENT")
    career = CareerAgent()
    ctx = await career.get_context(25, "Как войти в IT?", ["Изучить ML"])
    print(f"   Контекст: {ctx.guidelines[:100]}...")
    
    answer = await career.answer("Как войти в IT?", 25, ["Изучить ML"])
    print(f"   Ответ: {answer[:150]}...")
    
    # Creative Agent
    print("\n🎨 3. CREATIVE AGENT")
    creative = CreativeAgent()
    ctx = await creative.get_context(12, "Напиши историю про космос")
    print(f"   Тип: {ctx.metadata.get('type')}")
    
    story = await creative.create("Напиши историю про космос", 12, "story")
    print(f"   История: {story[:150]}...")
    
    print("\n" + "="*60)
    print("✨ Все агенты работают!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_agents())