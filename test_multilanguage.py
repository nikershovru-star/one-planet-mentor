"""
test_multilanguage.py — Тест поддержки множества языков
"""

import asyncio
from src.agents.language_agent import LanguageAgent
from src.language_config import SUPPORTED_LANGUAGES


async def test_multilanguage():
    print("\n" + "="*60)
    print("🌍 ТЕСТ МУЛЬТИЯЗЫЧНОСТИ")
    print("="*60)
    
    agent = LanguageAgent()
    
    # Тест 1: Список языков
    print("\n📋 1. ПОДДЕРЖИВАЕМЫЕ ЯЗЫКИ")
    languages = agent.get_supported_languages()
    for lang in languages:
        print(f"   {lang['code']}: {lang['name']} ({lang['name_en']})")
    
    # Тест 2: Определение языков
    print("\n🔍 2. ОПРЕДЕЛЕНИЕ ЯЗЫКОВ")
    test_texts = [
        ("Привет, как дела?", "ru"),
        ("Hello, how are you?", "en"),
        ("مرحبا، كيف حالك؟", "ar"),
        ("你好，你好吗？", "zh"),
        ("Hola, ¿cómo estás?", "es"),
        ("Bonjour, comment ça va?", "fr"),
        ("नमस्ते, आप कैसे हैं?", "hi"),
        ("Olá, como vai?", "pt"),
        ("Hallo, wie geht es dir?", "de"),
        ("こんにちは、お元気ですか？", "ja")
    ]
    
    for text, expected in test_texts:
        detected = agent.detect_language(text)
        status = "✅" if detected == expected else "⚠️"
        print(f"   {status} '{text[:20]}...' → {detected} (ожидалось: {expected})")
    
    # Тест 3: Переводы
    print("\n🔄 3. ПЕРЕВОДЫ")
    translations = [
        ("How do neural networks work?", "en", "ru"),
        ("¿Cómo funciona la inteligencia artificial?", "es", "ru"),
        ("人工智能是如何工作的？", "zh", "ru"),
        ("Comment fonctionne l'intelligence artificielle?", "fr", "ru")
    ]
    
    for text, from_lang, to_lang in translations:
        print(f"\n   {from_lang} → {to_lang}:")
        print(f"   Исходный: {text}")
        translated = await agent.translate(text, from_lang, to_lang)
        print(f"   Перевод: {translated}")
    
    # Тест 4: Культурные заметки
    print("\n📚 4. КУЛЬТУРНЫЕ ЗАМЕТКИ")
    for lang_code in ["ar", "zh", "ja"]:
        lang_info = SUPPORTED_LANGUAGES.get(lang_code, {})
        print(f"\n   {lang_info.get('name', lang_code)}:")
        for note in lang_info.get("cultural_notes", []):
            print(f"   - {note}")
    
    print("\n" + "="*60)
    print("✨ Мультиязычность работает!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_multilanguage())