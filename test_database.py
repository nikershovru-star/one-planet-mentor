"""
test_database.py — Тест сохранения и загрузки профилей
"""

from src.models import UserProfile
from src.database import save_user_profile, load_user_profile, get_user_stats


def test_database():
    print("\n" + "="*60)
    print("️  ТЕСТ БАЗЫ ДАННЫХ С ШИФРОВАНИЕМ")
    print("="*60)
    
    # Создаём тестовый профиль
    profile = UserProfile(
        user_id="test_user_123",
        age=25,
        religion="secular",
        language="ru",
        country="RU",
        goals=["Изучить ML", "Развить карьеру"],
        interests=["Наука", "Технологии"]
    )
    
    print(f"\n Исходный профиль:")
    print(f"  User ID: {profile.user_id}")
    print(f"  Возраст: {profile.age}")
    print(f"  Религия: {profile.religion}")
    print(f"  Цели: {profile.goals}")
    
    # Сохраняем (с шифрованием)
    print(f"\n💾 Сохраняем в БД...")
    user_hash = save_user_profile(profile)
    print(f"  ✅ Сохранено! Хэш ID: {user_hash[:20]}...")
    
    # Загружаем
    print(f"\n📂 Загружаем из БД...")
    loaded_profile = load_user_profile("test_user_123")
    
    if loaded_profile:
        print(f"  ✅ Загружено!")
        print(f"  User ID: {loaded_profile.user_id}")
        print(f"  Возраст: {loaded_profile.age}")
        print(f"  Религия: {loaded_profile.religion}")
        print(f"  Цели: {loaded_profile.goals}")
        
        # Проверяем что данные совпадают
        assert profile.age == loaded_profile.age
        assert profile.religion == loaded_profile.religion
        assert profile.goals == loaded_profile.goals
        print(f"\n  ✅ Все данные совпадают!")
    else:
        print(f"  ❌ Ошибка загрузки!")
    
    # Статистика
    print(f"\n📊 Статистика:")
    stats = get_user_stats()
    print(f"  Всего пользователей: {stats['total_users']}")
    print(f"  Распределение по возрастам: {stats['age_distribution']}")
    
    print("\n" + "="*60)
    print("✨ Тест завершён!")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_database()