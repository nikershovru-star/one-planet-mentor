"""
encryption.py — Шифрование чувствительных данных
Уникальный ключ для каждого пользователя
"""

import os
import hashlib
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


def get_master_key() -> bytes:
    """Получает мастер-ключ из .env."""
    key = os.getenv("MASTER_ENCRYPTION_KEY")
    
    if not key:
        # Генерируем новый мастер-ключ
        key = Fernet.generate_key().decode()
        print(f"️  Сгенерирован новый мастер-ключ. Добавь в .env:")
        print(f"MASTER_ENCRYPTION_KEY={key}")
        print(f"\n⚠️  ВАЖНО: Без этого ключа данные пользователей будут недоступны!")
        return key.encode()
    
    return key.encode()


def get_user_encryption_key(user_id: str) -> bytes:
    """Генерирует уникальный ключ шифрования для конкретного пользователя."""
    master_key = get_master_key()
    
    # Создаём уникальный ключ на основе user_id + master_key
    # Используем SHA-256 для детерминированной генерации
    combined = f"{user_id}:{master_key.decode()}"
    key_hash = hashlib.sha256(combined.encode()).digest()
    
    # Fernet требует 32-байтный ключ в base64
    import base64
    user_key = base64.urlsafe_b64encode(key_hash)
    
    return user_key


def encrypt_data(data: str, user_id: str) -> str:
    """Шифрует строку с ключом конкретного пользователя."""
    user_key = get_user_encryption_key(user_id)
    f = Fernet(user_key)
    encrypted = f.encrypt(data.encode())
    return encrypted.decode()


def decrypt_data(encrypted_data: str, user_id: str) -> str:
    """Расшифровывает строку с ключом конкретного пользователя."""
    user_key = get_user_encryption_key(user_id)
    f = Fernet(user_key)
    decrypted = f.decrypt(encrypted_data.encode())
    return decrypted.decode()


def hash_user_id(user_id: str) -> str:
    """Хэширует user_id для анонимизации (необратимо)."""
    return hashlib.sha256(user_id.encode()).hexdigest()