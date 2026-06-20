"""
search_agent.py — Агент поиска
DuckDuckGo (ddgs) + Wikipedia для актуальной информации
"""

import os
import json
from typing import List, Optional

from .base_agent import BaseAgent
from ..models import AgentContext


class SearchAgent(BaseAgent):
    """Поиск актуальной информации через DuckDuckGo и Wikipedia."""
    
    def __init__(self):
        super().__init__("search_agent")
        self.max_results = 5
    
    async def get_context(self, query: str, search_type: str = "web") -> AgentContext:
        """Выполняет поиск и возвращает контекст."""
        
        results = []
        
        if search_type == "web":
            results = await self.web_search(query)
        elif search_type == "wiki":
            results = await self.wikipedia_search(query)
        elif search_type == "news":
            results = await self.news_search(query)
        else:
            results = await self.web_search(query)
        
        return AgentContext(
            agent_name="search_agent",
            guidelines=json.dumps(results, ensure_ascii=False),
            metadata={
                "search_type": search_type,
                "results_count": len(results),
                "results": results
            }
        )
    
    async def web_search(self, query: str) -> List[dict]:
        """Поиск в интернете через DuckDuckGo (ddgs)."""
        
        try:
            from ddgs import DDGS
            
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_results))
            
            formatted = []
            for r in results:
                formatted.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", ""),
                    "source": "duckduckgo"
                })
            
            return formatted
            
        except Exception as e:
            print(f"⚠️  Ошибка DuckDuckGo: {e}")
            return []
    
    async def news_search(self, query: str) -> List[dict]:
        """Поиск новостей через DuckDuckGo."""
        
        try:
            from ddgs import DDGS
            
            with DDGS() as ddgs:
                results = list(ddgs.news(query, max_results=self.max_results))
            
            formatted = []
            for r in results:
                formatted.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("url", ""),
                    "source": r.get("source", ""),
                    "date": r.get("date", ""),
                    "type": "news"
                })
            
            return formatted
            
        except Exception as e:
            print(f"⚠️  Ошибка поиска новостей: {e}")
            return []
    
    async def wikipedia_search(self, query: str) -> List[dict]:
        """Поиск в Wikipedia через requests с правильными headers."""
        
        try:
            import requests
            
            # Wikipedia API с правильными headers
            url = "https://ru.wikipedia.org/w/api.php"
            headers = {
                "User-Agent": "OnePlanetMentor/1.0 (educational project)"
            }
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": 3
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            # Проверяем что ответ JSON
            if response.status_code != 200:
                print(f"⚠️  Wikipedia вернула статус {response.status_code}")
                return []
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"⚠️  Wikipedia вернула не JSON: {response.text[:100]}")
                return []
            
            results = data.get("query", {}).get("search", [])
            formatted = []
            
            for r in results:
                title = r.get("title", "")
                snippet = r.get("snippet", "").replace("<span class=\"searchmatch\">", "").replace("</span>", "")
                
                formatted.append({
                    "title": title,
                    "snippet": snippet[:300] + "..." if len(snippet) > 300 else snippet,
                    "url": f"https://ru.wikipedia.org/wiki/{title.replace(' ', '_')}",
                    "source": "wikipedia"
                })
            
            return formatted
            
        except Exception as e:
            print(f"⚠️  Ошибка Wikipedia: {e}")
            return []
    
    async def search_and_summarize(self, query: str, search_type: str = "web") -> str:
        """Поиск + краткое резюме результатов."""
        
        results = []
        
        if search_type == "web":
            results = await self.web_search(query)
        elif search_type == "wiki":
            results = await self.wikipedia_search(query)
        elif search_type == "news":
            results = await self.news_search(query)
        
        if not results:
            return "Не удалось найти информацию по запросу."
        
        # Формируем сводку
        summary_parts = []
        for i, r in enumerate(results[:3], 1):
            summary_parts.append(f"{i}. {r['title']}\n   {r['snippet']}")
        
        return "\n\n".join(summary_parts)