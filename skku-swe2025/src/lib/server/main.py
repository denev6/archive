import os

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from chatbot import SchoolChatbot

load_dotenv()

FAISS_INDEX = os.getenv("FAISS_INDEX")
ENCODER_MODEL = os.getenv("ENCODER_MODEL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_KEY = os.getenv("OPENAI_KEY")
TOP_K_DOCUMENTS = 3

# os.environ["OPENAI_API_KEY"] = OPENAI_KEY

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = SchoolChatbot(
    faiss_db=FAISS_INDEX,
    encoder=ENCODER_MODEL,
    top_k=TOP_K_DOCUMENTS,
    model_name=OPENAI_MODEL,
    api_key=OPENAI_KEY,
)


@app.get("/")
async def main():
    return {"msg": "Hello"}


@app.post("/answer")
async def stream_chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    async def event_generator():
        for chunk in chatbot.invoke_stream(user_input):
            if chunk:
                yield chunk

    return StreamingResponse(event_generator(), media_type="text/plain")
