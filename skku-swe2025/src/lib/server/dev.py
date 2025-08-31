import os

import gradio as gr
from dotenv import load_dotenv

from chatbot import SchoolChatbot

load_dotenv()

FAISS_INDEX = os.getenv("FAISS_INDEX")
ENCODER_MODEL = os.getenv("ENCODER_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
TOP_K_DOCUMENTS = 5

chatbot = SchoolChatbot(
    FAISS_INDEX, ENCODER_MODEL, TOP_K_DOCUMENTS, OPENAI_MODEL, OPENAI_API_KEY
)


def gradio_stream(user_input, history):
    partial_response = ""
    for chunk in chatbot.invoke_stream(user_input):
        partial_response += chunk
        yield partial_response


if __name__ == "__main__":
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    cuda_version = torch.version.cuda if device == "cuda" else ""
    is_debug = True
    print(f"⚠️ You are running dev version with debug={is_debug}")
    print(f"🔥 Torch device: {device} {cuda_version}")

    gr.ChatInterface(
        fn=gradio_stream,
        title="⚠️Test page",
        chatbot=gr.Chatbot(height=500, type="messages"),
        textbox=gr.Textbox(placeholder=f"Ask {OPENAI_MODEL}"),
        type="messages",
        theme="soft",
    ).launch(server_port=7861, debug=is_debug)
