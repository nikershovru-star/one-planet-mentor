"""
language_agent.py — Языковой агент с голосовыми функциями
Перевод, культурная адаптация, speech-to-text, text-to-speech
"""

import os
import json
from typing import Optional

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from .base_agent import BaseAgent
from ..models import AgentContext


class LanguageAgent(BaseAgent):
    """Перевод, культурная адаптация и голосовые функции."""
    
    def __init__(self):
        super().__init__("language_agent")
        model = os.getenv("LANGUAGE_AGENT_MODEL", "qwen3:14b")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.3
        )
        
        # Инициализация TTS
        self.tts_engine = None
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"⚠️  TTS не доступен: {e}")
    
    async def get_context(self, query: str, target_language: str = "ru") -> AgentContext:
        """Определяет язык запроса и даёт рекомендации по переводу."""
        
        detected_lang = self.detect_language(query)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — эксперт по языкам и культуре One Planet Mentor.
Определи язык запроса и дай рекомендации по переводу и культурной адаптации.

Формат (JSON):
{{
  "detected_language": "ru",
  "target_language": "ru",
  "needs_translation": false,
  "cultural_notes": ["заметка1", "заметка2"],
  "translation_style": "formal|informal|friendly"
}}

Отвечай ТОЛЬКО JSON."""),
            ("user", """Запрос: {query}
Целевой язык: {target_language}""")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "query": query,
            "target_language": target_language
        })
        
        try:
            text = response.content.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            lang_data = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            lang_data = {
                "detected_language": detected_lang,
                "target_language": target_language,
                "needs_translation": detected_lang != target_language,
                "cultural_notes": [],
                "translation_style": "friendly"
            }
        
        return AgentContext(
            agent_name="language_agent",
            guidelines=json.dumps(lang_data, ensure_ascii=False),
            metadata=lang_data
        )
    
    def detect_language(self, text: str) -> str:
        """Определяет язык текста с fallback для коротких текстов."""
        
        # Для коротких текстов langdetect ненадёжен — используем эвристику
        if len(text) < 20:
            if any('\u0400' <= c <= '\u04FF' for c in text):
                return "ru"
            elif any('\u4e00' <= c <= '\u9fff' for c in text):
                return "zh"
            elif any('\u0600' <= c <= '\u06FF' for c in text):
                return "ar"
            elif any('\u0900' <= c <= '\u097F' for c in text):
                return "hi"
            elif any('\u0530' <= c <= '\u058F' for c in text):
                return "hy"
        
        try:
            from langdetect import detect
            lang = detect(text)
            return lang
        except:
            return "unknown"
    
    async def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """Переводит текст с учётом культурного контекста."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — профессиональный переводчик One Planet Mentor.
Переведи текст с {from_lang} на {to_lang}.

ПРАВИЛА:
- Сохраняй смысл и тон
- Адаптируй идиомы под целевую культуру
- Используй естественный язык
- Не добавляй пояснения, только перевод"""),
            ("user", "{text}")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "from_lang": from_lang,
            "to_lang": to_lang,
            "text": text
        })
        
        return response.content
    
    def speak(self, text: str, language: str = "ru"):
        """Озвучивает текст голосом (text-to-speech)."""
        
        if not self.tts_engine:
            print("⚠️  TTS не доступен")
            return
        
        try:
            voices = self.tts_engine.getProperty('voices')
            
            if language == "ru":
                for voice in voices:
                    if 'russian' in voice.name.lower() or 'ru' in voice.id.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            elif language == "en":
                for voice in voices:
                    if 'english' in voice.name.lower() or 'en' in voice.id.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            print(f"⚠️  Ошибка TTS: {e}")
    
    def listen(self, timeout: int = 10) -> Optional[str]:
        """Слушает микрофон и распознаёт речь (speech-to-text)."""
        
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("🎙️  Говори... (или нажми Ctrl+C для отмены)")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=timeout)
            
            print("⏳  Распознаю речь...")
            
            try:
                text = recognizer.recognize_google(audio, language='ru-RU')
                return text
            except sr.UnknownValueError:
                print("⚠️  Не удалось распознать речь")
                return None
            except sr.RequestError as e:
                print(f"⚠️  Ошибка сервиса распознавания: {e}")
                return None
                
        except ImportError:
            print("️  SpeechRecognition не установлен")
            return None
        except Exception as e:
            print(f"⚠️  Ошибка записи: {e}")
            return None
    
    async def process_voice_message(self, audio_file: str, language: str = "ru") -> Optional[str]:
        """Обрабатывает голосовое сообщение из файла."""
        
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
            
            text = recognizer.recognize_google(audio, language=f'{language}-{language.upper()}')
            return text
            
        except Exception as e:
            print(f"⚠️  Ошибка обработки аудио: {e}")
            return None