"""
memory_agent.py — Агент памяти
Запоминает историю диалогов и предпочтения пользователя
"""

import os
import json
from datetime import datetime
from typing import List, Optional

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from .base_agent import BaseAgent
from ..models import AgentContext
from ..database import SessionLocal, UserRecord
from ..encryption import encrypt_data, decrypt_data


class MemoryAgent(BaseAgent):
    """Запоминает историю диалогов и извлекает релевантный контекст."""
    
    def __init__(self):
        super().__init__("memory_agent")
        model = os.getenv("MEMORY_AGENT_MODEL", "llama3:latest")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.3
        )
    
    async def get_context(self, user_id: str, query: str) -> AgentContext:
        """Извлекает релевантную память для текущего запроса."""
        
        # Загружаем историю из БД
        history = self._load_history(user_id)
        
        if not history:
            return AgentContext(
                agent_name="memory_agent",
                guidelines="Новый пользователь, истории нет.",
                metadata={"history_count": 0}
            )
        
        # Hermes3/llama3 решает что релевантно
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Ты — агент памяти One Planet Mentor.
Из истории диалогов пользователя выбери 2-3 самых релевантных факта для текущего запроса.

Формат ответа (JSON):
{{
  "relevant_facts": ["факт1", "факт2"],
  "user_preferences": {"ключ": "значение"},
  "conversation_summary": "краткое резюме"
}}

Отвечай ТОЛЬКО JSON."""),
            ("user", """История диалогов:
{history}

Текущий запрос: {query}""")
        ])
        
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "history": "\n".join(history[-10:]),  # Последние 10 сообщений
            "query": query
        })
        
        try:
            text = response.content.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            memory_data = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            memory_data = {
                "relevant_facts": [],
                "user_preferences": {},
                "conversation_summary": ""
            }
        
        return AgentContext(
            agent_name="memory_agent",
            guidelines=json.dumps(memory_data, ensure_ascii=False),
            metadata={
                "history_count": len(history),
                "memory_data": memory_data
            }
        )
    
    def save_interaction(self, user_id: str, query: str, response: str):
        """Сохраняет взаимодействие в БД."""
        db = SessionLocal()
        try:
            from ..encryption import hash_user_id
            user_hash = hash_user_id(user_id)
            record = db.query(UserRecord).filter_by(user_id_hash=user_hash).first()
            
            if record:
                # Добавляем в существующую запись
                current_history = record.goals_encrypted or ""
                new_entry = f"[{datetime.utcnow().isoformat()}] Q: {query} | A: {response[:200]}"
                updated = f"{current_history}\n{new_entry}" if current_history else new_entry
                record.goals_encrypted = encrypt_data(updated, user_id)
                db.commit()
        finally:
            db.close()
    
    def _load_history(self, user_id: str) -> List[str]:
        """Загружает историю диалогов."""
        db = SessionLocal()
        try:
            from ..encryption import hash_user_id
            user_hash = hash_user_id(user_id)
            record = db.query(UserRecord).filter_by(user_id_hash=user_hash).first()
            
            if record and record.goals_encrypted:
                try:
                    history_text = decrypt_data(record.goals_encrypted, user_id)
                    return [line for line in history_text.split("\n") if line.strip()]
                except Exception:
                    return []
            return []
        finally:
            db.close()