import os
import openai
from google import genai
from google.genai import types
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_KEY")


def ask_gemini(prompt):
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=3)
        ),
    )
    result = response.text
    return result


def ask_gpt(prompt):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-mini-2025-04-14",
        messages=[{"role": "user", "content": prompt}],
    )
    result = response.choices[0].message.content
    return result


def ask_anthropic(prompt):
    client = Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))
    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    result = message.content[0].text
    return result
