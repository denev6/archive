import json
from ai_models import *

RESULT_TXT = "responses/woh_gpt-4.1-2025-04-14.txt"

with open("doc_without_header.json", "r", encoding="utf-8") as f:
    doc = json.load(f)

PROMPT = f"""제목:\n{doc['content']}\n본문:\n{doc['content']}\n\n이 내용을 읽고 핵심을 요약해줘"""

response = ask_gpt(PROMPT)

with open(RESULT_TXT, "w", encoding="utf-8") as f:
    f.write(response)
