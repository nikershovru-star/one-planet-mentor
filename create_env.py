"""
create_env.py — Создаёт .env файл с правильным ключом
"""
from cryptography.fernet import Fernet

# Генерируем ключ
key = Fernet.generate_key().decode()

# Создаём .env файл
content = f"""OLLAMA_BASE_URL=http://localhost:11434
AGE_AGENT_MODEL=llama3:latest
FAITH_AGENT_MODEL=qwen3:14b
SCIENCE_AGENT_MODEL=qwen3:14b
SAFETY_AGENT_MODEL=llama3:latest
MASTER_ENCRYPTION_KEY={key}
DB_PATH=one_planet_mentor.db
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Файл .env создан!")
print(f"🔑 Твой мастер-ключ: {key}")
print("\n⚠️  СОХРАНИ ЭТОТ КЛЮЧ! Без него данные будут недоступны!")