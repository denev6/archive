import os
import json
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_KEY"))

results = client.search(
    query="Search the URL: https://denev6.tistory.com/entry/til-3",
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    max_results=1,
)

# 결과 출력
for result in results["results"]:
    r = {
        "title": result["title"],
        "content": result["content"],
        "raw_content": result["raw_content"],
    }
    with open("docs_tavily.json", "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)

    break
