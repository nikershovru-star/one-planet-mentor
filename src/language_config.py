"""
language_config.py — Конфигурация языков и культур
"""

# Поддерживаемые языки
SUPPORTED_LANGUAGES = {
    "ru": {
        "name": "Русский",
        "name_en": "Russian",
        "tts_code": "ru-RU",
        "stt_code": "ru-RU",
        "direction": "ltr",
        "cultural_notes": [
            "Используйте формальное обращение на 'вы' для взрослых",
            "Цените прямолинейность и честность",
            "Уважайте старших по возрасту"
        ]
    },
    "en": {
        "name": "English",
        "name_en": "English",
        "tts_code": "en-US",
        "stt_code": "en-US",
        "direction": "ltr",
        "cultural_notes": [
            "Use first names in informal settings",
            "Value directness and clarity",
            "Respect personal space and privacy"
        ]
    },
    "ar": {
        "name": "العربية",
        "name_en": "Arabic",
        "tts_code": "ar-SA",
        "stt_code": "ar-SA",
        "direction": "rtl",
        "cultural_notes": [
            "Используйте уважительные титулы",
            "Избегайте тем, связанных с религией, если не запрошено",
            "Цените гостеприимство и щедрость"
        ]
    },
    "zh": {
        "name": "中文",
        "name_en": "Chinese",
        "tts_code": "zh-CN",
        "stt_code": "zh-CN",
        "direction": "ltr",
        "cultural_notes": [
            "Используйте формальные обращения",
            "Уважайте иерархию и возраст",
            "Цените гармонию и коллективизм"
        ]
    },
    "es": {
        "name": "Español",
        "name_en": "Spanish",
        "tts_code": "es-ES",
        "stt_code": "es-ES",
        "direction": "ltr",
        "cultural_notes": [
            "Используйте 'tú' для неформального общения",
            "Цените семейные связи",
            "Будьте теплым и дружелюбным"
        ]
    },
    "fr": {
        "name": "Français",
        "name_en": "French",
        "tts_code": "fr-FR",
        "stt_code": "fr-FR",
        "direction": "ltr",
        "cultural_notes": [
            "Используйте 'vous' для формального общения",
            "Цените интеллектуальные дискуссии",
            "Уважайте культурное наследие"
        ]
    },
    "hi": {
        "name": "हिन्दी",
        "name_en": "Hindi",
        "tts_code": "hi-IN",
        "stt_code": "hi-IN",
        "direction": "ltr",
        "cultural_notes": [
            "Используйте уважительные обращения",
            "Уважайте старших и учителей",
            "Цените духовность и традиции"
        ]
    },
    "pt": {
        "name": "Português",
        "name_en": "Portuguese",
        "tts_code": "pt-BR",
        "stt_code": "pt-BR",
        "direction": "ltr",
        "cultural_notes": [
            "Будьте дружелюбным и неформальным",
            "Цените семейные связи",
            "Используйте уменьшительно-ласкательные формы"
        ]
    },
    "de": {
        "name": "Deutsch",
        "name_en": "German",
        "tts_code": "de-DE",
        "stt_code": "de-DE",
        "direction": "ltr",
        "cultural_notes": [
            "Используйте 'Sie' для формального общения",
            "Цените точность и пунктуальность",
            "Будьте прямым и конкретным"
        ]
    },
    "ja": {
        "name": "日本語",
        "name_en": "Japanese",
        "tts_code": "ja-JP",
        "stt_code": "ja-JP",
        "direction": "ltr",
        "cultural_notes": [
            "Используйте вежливые формы речи",
            "Уважайте иерархию",
            "Цените гармонию и групповую динамику"
        ]
    }
}

# Маппинг кодов языков для langdetect
LANGDETECT_MAPPING = {
    "ru": "ru",
    "en": "en",
    "ar": "ar",
    "zh": "zh-cn",
    "es": "es",
    "fr": "fr",
    "hi": "hi",
    "pt": "pt",
    "de": "de",
    "ja": "ja"
}

# Приоритетные языки для TTS (если доступно)
TTS_PRIORITY = ["en", "ru", "es", "fr", "de"]