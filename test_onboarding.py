"""
test_onboarding.py — Тест системы онбординга
"""

from src.onboarding import (
    ONBOARDING_QUESTIONS,
    OnboardingAnswers,
    map_religion,
    map_age_range,
    map_language,
    create_user_profile,
    format_welcome_message
)


def simulate_onboarding():
    """Симулирует прохождение анкеты."""
    
    print("\n" + "="*60)
    print("🌍 ONE PLANET MENTOR — АНКЕТА")
    print("="*60)
    print("\nПривет! Я твой AI-наставник. Давай познакомимся!\n")
    
    # Симулируем ответы пользователя
    answers_data = {
        "age": 25,
        "religion": "secular",
        "language": "ru",
        "country": "RU",
        "goals": ["Изучить новый предмет", "Развить карьеру"],
        "interests": ["Наука и технологии", "Бизнес и финансы"],
        "communication_style": "friendly",
        "experience_level": "beginner"
    }
    
    answers = OnboardingAnswers(**answers_data)
    
    print("✅ Анкета заполнена:\n")
    print(f"  Возраст: {answers.age} лет")
    print(f"  Мировоззрение: {answers.religion}")
    print(f"  Язык: {answers.language}")
    print(f"  Страна: {answers.country}")
    print(f"  Цели: {', '.join(answers.goals)}")
    print(f"  Интересы: {', '.join(answers.interests)}")
    print(f"  Стиль общения: {answers.communication_style}")
    print(f"  Уровень: {answers.experience_level}")
    
    # Создаём профиль
    profile = create_user_profile(answers, user_id="test_user_001")
    
    print(f"\n Профиль создан:")
    print(f"  User ID: {profile.user_id}")
    print(f"  Age group: {profile.age}")
    
    # Приветственное сообщение
    welcome = format_welcome_message(profile)
    print(f"\n Приветствие: {welcome}")
    
    print("\n" + "="*60)
    print("✨ Теперь наставник знает о тебе и готов помочь!")
    print("="*60 + "\n")
    
    return profile


if __name__ == "__main__":
    simulate_onboarding()