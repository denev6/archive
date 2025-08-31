import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_data(dir_path: str) -> list[str]:
    all_files_content = []
    if not os.path.isdir(dir_path):
        print(f"Error: Directory '{dir_path}' not found.")
        return all_files_content

    for filename in os.listdir(dir_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(dir_path, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    all_files_content.append(content)
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
    return all_files_content


def create_documents(data, chunk_size: int, chunk_overlap: int):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = []
    for text in data:
        chunks = text_splitter.split_text(text)
        for chunk in chunks:
            doc = Document(page_content=chunk)
            docs.append(doc)
    return docs


def embed(encoder, dir_path, faiss_path):
    data = load_data(dir_path)
    docs = create_documents(data, chunk_size=1000, chunk_overlap=100)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Embedding vectors on {device}...")
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=encoder, model_kwargs={"device": device}
    )
    faiss_index = FAISS.from_documents(docs, hf_embeddings)

    os.makedirs(faiss_path, exist_ok=True)
    faiss_index.save_local(folder_path=faiss_path)
    print(f"FAISS index saved to folder: {faiss_path}")


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    ENCODER_MODEL = os.getenv("ENCODER_MODEL")
    FAISS_INDEX = os.getenv("FAISS_INDEX")
    DIR_PATH = "sample"

    embed(ENCODER_MODEL, DIR_PATH, FAISS_INDEX)
