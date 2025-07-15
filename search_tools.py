from ddgs import DDGS
from agents import function_tool

@function_tool
def search_duckduckgo(query: str) -> list[dict]:
    "Search the web using DuckDuckGo"
    with DDGS() as ddgs:
        results = ddgs.text(query)
        return [
            {"title": r["title"], "href": r["href"], "body": r["body"]}
            for r in results[:5]
        ]
