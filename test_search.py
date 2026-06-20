"""
test_search.py — Тест Search Agent
"""

import asyncio
from src.agents.search_agent import SearchAgent


async def test_search():
    print("\n" + "="*60)
    print("🔍 ТЕСТ SEARCH AGENT")
    print("="*60)
    
    agent = SearchAgent()
    
    # Тест 1: Веб-поиск
    print("\n🌐 1. ВЕБ-ПОИСК (DuckDuckGo)")
    results = await agent.web_search("нейронные сети 2025")
    print(f"   Найдено результатов: {len(results)}")
    for i, r in enumerate(results[:3], 1):
        print(f"\n   {i}. {r['title']}")
        print(f"      {r['snippet'][:100]}...")
        print(f"      URL: {r['url']}")
    
    # Тест 2: Wikipedia
    print("\n\n📚 2. WIKIPEDIA")
    wiki_results = await agent.wikipedia_search("искусственный интеллект")
    print(f"   Найдено статей: {len(wiki_results)}")
    for i, r in enumerate(wiki_results[:2], 1):
        print(f"\n   {i}. {r['title']}")
        print(f"      {r['snippet'][:150]}...")
    
    # Тест 3: Новости
    print("\n\n📰 3. НОВОСТИ")
    news_results = await agent.news_search("AI новости")
    print(f"   Найдено новостей: {len(news_results)}")
    for i, r in enumerate(news_results[:3], 1):
        print(f"\n   {i}. {r['title']}")
        print(f"      Источник: {r.get('source', 'unknown')}")
        print(f"      Дата: {r.get('date', 'unknown')}")
    
    # Тест 4: Поиск + резюме
    print("\n\n📝 4. ПОИСК + РЕЗЮМЕ")
    summary = await agent.search_and_summarize("квантовые компьютеры", "wiki")
    print(f"   {summary[:300]}...")
    
    print("\n" + "="*60)
    print("✨ Search Agent работает!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_search())