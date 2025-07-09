import json
from ddgs import DDGS

query = "Search the URL: https://denev6.tistory.com/entry/til-3"

with DDGS() as ddgs:
    for r in ddgs.text(query, max_results=1):
        with open("docs_duck.json", "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=2)
