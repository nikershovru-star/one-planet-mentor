"""
test_language_agent.py — Тест языкового агента
"""

import asyncio
from src.agents.language_agent import LanguageAgent


async def test_language_agent():
    print("\n" + "="*60)
    print(" ТЕСТ LANGUAGE AGENT")
    print("="*60)
    
    agent = LanguageAgent()
    
    # Тест 1: Определение языка
    print("\n🔍 1. ОПРЕДЕЛЕНИЕ ЯЗЫКА")
    texts = [
        "Привет, как дела?",
        "Hello, how are you?",
        "Hola, ¿cómo estás?",
        "Bonjour, comment ça va?"
    ]
    
    for text in texts:
        lang = agent.detect_language(text)
        print(f"   '{text}' → {lang}")
    
    # Тест 2: Контекст
    print("\n📋 2. АНАЛИЗ КОНТЕКСТА")
    ctx = await agent.get_context("Hello, how do neural networks work?", "ru")
    print(f"   Обнаруженный язык: {ctx.metadata.get('detected_language')}")
    print(f"   Нужен перевод: {ctx.metadata.get('needs_translation')}")
    print(f"   Культурные заметки: {ctx.metadata.get('cultural_notes')}")
    
    # Тест 3: Перевод
    print("\n🔄 3. ПЕРЕВОД")
    translation = await agent.translate(
        "How do neural networks work?",
        "en",
        "ru"
    )
    print(f"   EN → RU: {translation}")
    
    # Тест 4: TTS (опционально)
    print("\n 4. TEXT-TO-SPEECH")
    print("   (Если слышишь голос — всё работает!)")
    agent.speak("Привет! Я твой AI-наставник.", "ru")
    
    # Тест 5: Voice Input (опционально)
    print("\n🎙️ 5. SPEECH-TO-TEXT")
    print("   Скажи что-нибудь в микрофон...")
    voice_text = agent.listen(timeout=5)
    if voice_text:
        print(f"   Распознано: {voice_text}")
    else:
        print("   Голосовой ввод пропущен")
    
    print("\n" + "="*60)
    print("✨ Language Agent работает!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_language_agent())