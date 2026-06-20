#!/usr/bin/env python3
"""
run_demo.py — Демонстрация работы One Planet Mentor
Запускает orchestrator с 3 разными пользователями.
"""

import asyncio
import os
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

from src.models import UserProfile, Query
from src.orchestrator import Orchestrator


async def main():
    print("\n🌍 One Planet Mentor — Multi-Agent Demo")
    print("=" * 50)
    
    orchestrator = Orchestrator()
    
    # ============================================
    # Пример 1: 12-летняя девочка из Бразилии (католичка)
    # ============================================
    user1 = UserProfile(
        user_id="maria_12_br",
        age=12,
        religion="christian",
        language="pt",
        country="BR",
        goals=["учиться науке", "готовиться к школе"]
    )
    
    query1 = Query(
        text="Почему небо голубое?",
        user=user1
    )
    
    print("\n📝 Query 1: \"Почему небо голубое?\"")
    print("   👤 User: 12 лет, Бразилия, Christian")
    response1 = await orchestrator.process(query1)
    print("   🤖 Response:")
    print("   " + response1.text.replace("\n", "\n   "))
    print(f"   ⏱️  Latency: {response1.latency_ms}ms")
    
    # ============================================
    # Пример 2: 70-летний дедушка из Саудовской Аравии (мусульманин)
    # ============================================
    user2 = UserProfile(
        user_id="ahmed_70_sa",
        age=70,
        religion="muslim",
        language="ar",
        country="SA",
        goals=["объяснить внукам науку", "оставаться активным"]
    )
    
    query2 = Query(
        text="Что такое гравитация? Хочу объяснить внукам.",
        user=user2
    )
    
    print("\n\n📝 Query 2: \"Что такое гравитация?\"")
    print("   👤 User: 70 лет, Saudi Arabia, Muslim")
    response2 = await orchestrator.process(query2)
    print("   🤖 Response:")
    print("   " + response2.text.replace("\n", "\n   "))
    print(f"   ⏱️  Latency: {response2.latency_ms}ms")
    
    # ============================================
    # Пример 3: 25-летний программист из Швеции (светский гуманист)
    # ============================================
    user3 = UserProfile(
        user_id="erik_25_se",
        age=25,
        religion="secular",
        language="sv",
        country="SE",
        goals=["изучить ML", "карьера в IT"]
    )
    
    query3 = Query(
        text="Как работают нейронные сети?",
        user=user3
    )
    
    print("\n\n📝 Query 3: \"Как работают нейронные сети?\"")
    print("   👤 User: 25 лет, Sweden, Secular")
    response3 = await orchestrator.process(query3)
    print("   🤖 Response:")
    print("   " + response3.text.replace("\n", "\n   "))
    print(f"   ⏱️  Latency: {response3.latency_ms}ms")
    
    print("\n\n✨ Demo complete! 3 персонализированных ответа.")
    print("🌍 One Planet — One Mentor — 8 Billion People")


if __name__ == "__main__":
    asyncio.run(main())