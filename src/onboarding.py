"""
onboarding.py — Анкета для первого взаимодействия
Собирает информацию о пользователе для персонализации.
"""

from typing import Optional, List
from pydantic import BaseModel, Field
from .models import UserProfile


class OnboardingQuestion(BaseModel):
    """Один вопрос анкеты."""
    
    id: str
    text: str
    type: str  # "choice", "text", "multiple_choice"
    options: Optional[List[str]] = None
    required: bool = True
    default: Optional[str] = None


class OnboardingAnswers(BaseModel):
    """Ответы пользователя на анкету."""
    
    age: int = Field(..., ge=5, le=99, description="Возраст")
    religion: str = Field(default="unspecified", description="Религиозный контекст")
    language: str = Field(default="ru", description="Предпочтительный язык")
    country: Optional[str] = Field(default=None, description="Страна")
    goals: List[str] = Field(default_factory=list, description="Цели обучения")
    interests: List[str] = Field(default_factory=list, description="Интересы")
    communication_style: str = Field(default="friendly", description="Стиль общения")
    experience_level: str = Field(default="beginner", description="Уровень подготовки")


# Вопросы анкеты
ONBOARDING_QUESTIONS = [
    OnboardingQuestion(
        id="age",
        text="Сколько тебе лет?",
        type="choice",
        options=["5-8", "9-11", "12-14", "15-17", "18-21", "22-25", "26-30", "31-60", "60-99"],
        required=True
    ),
    OnboardingQuestion(
        id="religion",
        text="К какой традиции ты себя относишь? (это поможет мне лучше понимать тебя)",
        type="choice",
        options=[
            "Христианство",
            "Ислам",
            "Иудаизм",
            "Буддизм",
            "Индуизм",
            "Светский гуманизм",
            "Предпочитаю не указывать"
        ],
        required=False,
        default="Предпочитаю не указывать"
    ),
    OnboardingQuestion(
        id="language",
        text="На каком языке тебе удобнее общаться?",
        type="choice",
        options=["Русский", "English", "Español", "العربية", "中文", "Другой"],
        required=True,
        default="Русский"
    ),
    OnboardingQuestion(
        id="goals",
        text="Чего ты хочешь достичь с помощью наставника? (можно несколько)",
        type="multiple_choice",
        options=[
            "Изучить новый предмет",
            "Подготовиться к экзамену",
            "Развить карьеру",
            "Найти хобби",
            "Улучшить здоровье",
            "Изучить языки",
            "Творческое развитие",
            "Духовный рост"
        ],
        required=True
    ),
    OnboardingQuestion(
        id="interests",
        text="Что тебя больше всего интересует? (можно несколько)",
        type="multiple_choice",
        options=[
            "Наука и технологии",
            "Искусство и культура",
            "Спорт и здоровье",
            "Бизнес и финансы",
            "Путешествия",
            "Природа и экология",
            "История и философия",
            "Кулинария"
        ],
        required=True
    ),
    OnboardingQuestion(
        id="communication_style",
        text="Какой стиль общения тебе ближе?",
        type="choice",
        options=[
            "Дружелюбный и неформальный",
            "Профессиональный и структурированный",
            "Вдохновляющий и мотивирующий",
            "Спокойный и вдумчивый"
        ],
        required=True,
        default="Дружелюбный и неформальный"
    ),
    OnboardingQuestion(
        id="experience_level",
        text="Какой у тебя уровень подготовки в интересующих темах?",
        type="choice",
        options=["Новичок", "Средний", "Продвинутый", "Эксперт"],
        required=True,
        default="Новичок"
    )
]


def map_religion(answer: str) -> str:
    """Маппинг ответов на внутренние коды."""
    mapping = {
        "Христианство": "christian",
        "Ислам": "muslim",
        "Иудаизм": "jewish",
        "Буддизм": "buddhist",
        "Индуизм": "hindu",
        "Светский гуманизм": "secular",
        "Предпочитаю не указывать": "unspecified"
    }
    return mapping.get(answer, "unspecified")


def map_age_range(answer: str) -> int:
    """Маппинг возрастного диапазона на конкретный возраст (середина)."""
    mapping = {
        "5-8": 6,
        "9-11": 10,
        "12-14": 13,
        "15-17": 16,
        "18-21": 19,
        "22-25": 23,
        "26-30": 28,
        "31-60": 45,
        "60-99": 75
    }
    return mapping.get(answer, 25)


def map_language(answer: str) -> str:
    """Маппинг языка на ISO код."""
    mapping = {
        "Русский": "ru",
        "English": "en",
        "Español": "es",
        "العربية": "ar",
        "中文": "zh",
        "Другой": "en"
    }
    return mapping.get(answer, "en")


def create_user_profile(answers: OnboardingAnswers, user_id: str) -> UserProfile:
    """Создаёт профиль пользователя из ответов анкеты."""
    return UserProfile(
        user_id=user_id,
        age=answers.age,
        religion=answers.religion,
        language=answers.language,
        country=answers.country,
        goals=answers.goals,
        interests=answers.interests
    )


def format_welcome_message(profile: UserProfile) -> str:
    """Формирует приветственное сообщение на основе профиля."""
    from .models import get_age_group
    
    age_group = get_age_group(profile.age)
    
    messages = {
        "toddlers": f"Привет! 🌟 Мне {profile.age} лет, и я хочу учиться!",
        "kids": f"Привет! 👋 Мне {profile.age} лет, я в {age_group} группе!",
        "preteens": f"Здравствуй! 😊 Мне {profile.age} лет, хочу узнать много нового!",
        "teens": f"Привет! 🚀 Мне {profile.age} лет, ищу свой путь!",
        "students": f"Привет! 🎓 Мне {profile.age} лет, учусь и развиваюсь!",
        "young_adults": f"Здравствуйте! 💼 Мне {profile.age} лет, строю карьеру!",
        "professionals": f"Здравствуйте!  Мне {profile.age} лет, хочу расти профессионально!",
        "mature": f"Здравствуйте! 🌱 Мне {profile.age} лет, никогда не поздно учиться!",
        "elders": f"Здравствуйте! 🌍 Мне {profile.age} лет, хочу делиться опытом и узнавать новое!"
    }
    
    return messages.get(age_group, f"Привет! Мне {profile.age} лет!")