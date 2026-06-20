#!/usr/bin/env python3
"""
run_demo.py — Демонстрация работы One Planet Mentor с анкетой
"""

import asyncio
from dotenv import load_dotenv

load_dotenv()

from src.models import UserProfile, Query
from src.orchestrator import Orchestrator
from src.onboarding import OnboardingAnswers, create_user_profile


async def main():
    print("\n🌍 One Planet Mentor — Demo с анкетой")
    print("=" * 60)
    
    # ============================================
    # Шаг 1: Пользователь заполняет анкету
    # ============================================
    print("\n📋 ШАГ 1: Заполнение анкеты\n")
    
    answers = OnboardingAnswers(
        age=25,
        religion="secular",
        language="ru",
        country="RU",
        goals=["Изучить ML", "Развить карьеру"],
        interests=["Наука и технологии", "Бизнес"],
        communication_style="friendly",
        experience_level="beginner"
    )
    
    print(f"  ✅ Возраст: {answers.age}")
    print(f"  ✅ Мировоззрение: {answers.religion}")
    print(f"  ✅ Язык: {answers.language}")
    print(f"  ✅ Цели: {answers.goals}")
    
    # Создаём профиль из анкеты
    profile = create_user_profile(answers, user_id="demo_user_001")
    
    print(f"\n🎯 Профиль создан для пользователя {profile.user_id}")
    
    # ============================================
    # Шаг 2: Задаём вопросы
    # ============================================
    print("\n" + "="*60)
    print("💬 ШАГ 2: Общение с наставником\n")
    
    orchestrator = Orchestrator()
    
    queries = [
        "Как работают нейронные сети?",
        "С чего начать изучение машинного обучения?",
        "Какие навыки нужны для карьеры в IT?"
    ]
    
    for i, query_text in enumerate(queries, 1):
        print(f"\n📝 Вопрос {i}: \"{query_text}\"")
        
        query = Query(text=query_text, user=profile)
        response = await orchestrator.process(query)
        
        print(f"   🤖 Ответ:")
        print(f"   {response.text[:200]}...")
        print(f"   ⏱️  {response.latency_ms}ms")
    
    print("\n\n✨ Demo complete!")
    print("🌍 One Planet — One Mentor — 8 Billion People")


if __name__ == "__main__":
    asyncio.run(main())