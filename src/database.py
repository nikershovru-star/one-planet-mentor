"""
database.py — База данных для хранения профилей
SQLite + уникальное шифрование для каждого пользователя
"""

import os
from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from .encryption import encrypt_data, decrypt_data, hash_user_id
from .models import UserProfile

# Путь к базе данных
DB_PATH = os.getenv("DB_PATH", "one_planet_mentor.db")

# Создаём engine
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Создаём сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class UserRecord(Base):
    """Таблица пользователей в БД."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id_hash = Column(String, unique=True, index=True)
    age = Column(Integer)
    religion_encrypted = Column(Text)
    language = Column(String, default="ru")
    country = Column(String, nullable=True)
    goals_encrypted = Column(Text)
    interests_encrypted = Column(Text)
    communication_style = Column(String, default="friendly")
    experience_level = Column(String, default="beginner")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def save_user_profile(profile: UserProfile) -> str:
    """Сохраняет профиль пользователя в БД с уникальным шифрованием."""
    
    db = SessionLocal()
    try:
        user_id_hash = hash_user_id(profile.user_id)
        
        existing = db.query(UserRecord).filter_by(user_id_hash=user_id_hash).first()
        
        if existing:
            existing.age = profile.age
            existing.religion_encrypted = encrypt_data(profile.religion, profile.user_id)
            existing.language = profile.language
            existing.country = profile.country
            existing.goals_encrypted = encrypt_data(",".join(profile.goals), profile.user_id)
            existing.interests_encrypted = encrypt_data(",".join(profile.interests), profile.user_id)
            existing.last_active = datetime.utcnow()
            user_record = existing
        else:
            user_record = UserRecord(
                user_id_hash=user_id_hash,
                age=profile.age,
                religion_encrypted=encrypt_data(profile.religion, profile.user_id),
                language=profile.language,
                country=profile.country,
                goals_encrypted=encrypt_data(",".join(profile.goals), profile.user_id),
                interests_encrypted=encrypt_data(",".join(profile.interests), profile.user_id),
                communication_style="friendly",
                experience_level="beginner"
            )
            db.add(user_record)
        
        db.commit()
        db.refresh(user_record)
        
        return user_id_hash
        
    finally:
        db.close()


def load_user_profile(user_id: str) -> Optional[UserProfile]:
    """Загружает профиль пользователя из БД."""
    
    db = SessionLocal()
    try:
        user_id_hash = hash_user_id(user_id)
        record = db.query(UserRecord).filter_by(user_id_hash=user_id_hash).first()
        
        if not record:
            return None
        
        religion = decrypt_data(record.religion_encrypted, user_id)
        goals = decrypt_data(record.goals_encrypted, user_id).split(",") if record.goals_encrypted else []
        interests = decrypt_data(record.interests_encrypted, user_id).split(",") if record.interests_encrypted else []
        
        return UserProfile(
            user_id=user_id,
            age=record.age,
            religion=religion,
            language=record.language,
            country=record.country,
            goals=goals,
            interests=interests
        )
        
    finally:
        db.close()


def get_user_stats() -> dict:
    """Получает статистику пользователей (анонимно)."""
    
    db = SessionLocal()
    try:
        total_users = db.query(UserRecord).count()
        
        age_stats = {}
        for record in db.query(UserRecord).all():
            from .models import get_age_group
            group = get_age_group(record.age)
            age_stats[group] = age_stats.get(group, 0) + 1
        
        return {
            "total_users": total_users,
            "age_distribution": age_stats
        }
        
    finally:
        db.close()