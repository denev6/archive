import os

import torch
from dotenv import load_dotenv
from huggingface_hub import login
from sentence_transformers import SentenceTransformer

ENV_PATH = ".env"

if not os.path.exists(ENV_PATH):
    raise FileNotFoundError(f"{ENV_PATH} not found.")

load_dotenv(ENV_PATH)
HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")
ENCODER = os.getenv("ENCODER_MODEL")

login(token=HUGGINGFACE_KEY)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Installing encoder for {device}...")
model = SentenceTransformer(ENCODER, device=device)
model.save(ENCODER)
