import time
import threading
from queue import Queue

from langchain_openai import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def get_free_ChatModel(model, api_key, **kwargs) -> ChatOpenAI:
    ANTHROPIC_MODELS = ["claude-3-haiku-20240307", "claude-3-7-sonnet-20250219"]
    OPENAI_MODELS = [
        # 무료 토큰을 제공하는 모델입니다 :)
        "gpt-4o-mini-2024-07-18",
        "gpt-4.1-mini-2025-04-14",
        "gpt-4.1-nano-2025-04-14",
    ]
    if model in OPENAI_MODELS:
        return ChatOpenAI(model=model, api_key=api_key, **kwargs)
    else:
        raise ValueError(f"Only support: {ANTHROPIC_MODELS + OPENAI_MODELS}")


class StreamCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.buffer = Queue()

    def reset_buffer(self):
        self.buffer = Queue()

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.buffer.put(token)

    def get_buffer(self):
        return self.buffer.get()


class SchoolChatbot:
    def __init__(
        self,
        faiss_db,
        encoder,
        top_k,
        model_name,
        api_key,
    ):
        # Retriever and LLM
        hf_embeddings = HuggingFaceEmbeddings(model_name=encoder)
        faiss_index = FAISS.load_local(
            faiss_db, hf_embeddings, allow_dangerous_deserialization=True
        )
        self.retriever = faiss_index.as_retriever(
            search_type="similarity", search_kwargs={"k": top_k}
        )
        self.stream_handler = StreamCallbackHandler()
        self.llm = get_free_ChatModel(
            model=model_name,
            api_key=api_key,
            temperature=0.2,
            max_tokens=512,
            streaming=True,
            callbacks=[self.stream_handler],
        )

        # Chat History (single session)
        self.history_key = "chat_history"
        self.session_history = ChatMessageHistory()

        # Runnable
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an assistant for question-answering tasks. 
                    Use the following pieces of retrieved context to answer the question. 
                    If you don't know the answer, just say that you don't know. 
                    Always answer in Korean if the user asked in Korean.
                    """,
                ),
                MessagesPlaceholder(variable_name=self.history_key),
                ("human", "{input}"),
            ]
        )
        runnable = prompt_template | self.llm
        self.with_message_history = RunnableWithMessageHistory(
            runnable,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key=self.history_key,
        )

    def get_session_history(self) -> BaseChatMessageHistory:
        return self.session_history

    def retrieve(self, query):
        documents = self.retriever.invoke(query)
        return documents

    def generate_prompt(self, user_query):
        documents = self.retrieve(user_query)
        if documents:
            reference_documents = "\n".join(
                f"- '{document.page_content}'" for document in documents
            )
        else:
            reference_documents = ""

        user_prompt = f"""
        Question: {user_query} 
        Context:
        {reference_documents} 
        Answer
        """
        return user_prompt

    def invoke_stream(self, user_query, num_recent_history=3):
        history = self.get_session_history()
        num_recent_history = min(len(history.messages), num_recent_history)
        history.messages = history.messages[-num_recent_history:]

        self.stream_handler.reset_buffer()
        user_prompt = self.generate_prompt(user_query.strip())

        def run_chain():
            self.with_message_history.invoke({"input": user_prompt})

        thread = threading.Thread(target=run_chain)
        thread.start()

        # Streaming loop
        while thread.is_alive():
            chunk = self.stream_handler.get_buffer()
            yield chunk
            time.sleep(0.05)

        # Final flush in case any leftover
        while not self.stream_handler.buffer.empty():
            chunk = self.stream_handler.get_buffer()
            yield chunk
            time.sleep(0.05)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    FAISS_INDEX = os.getenv("FAISS_INDEX")
    ENCODER_MODEL = os.getenv("ENCODER_MODEL")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    TOP_K_DOCUMENTS = 3

    chatbot = SchoolChatbot(
        FAISS_INDEX, ENCODER_MODEL, TOP_K_DOCUMENTS, OPENAI_MODEL, OPENAI_KEY
    )
    for chunk in chatbot.invoke_stream(
        "소프트웨어 테스팅에 대해 배울 수 있는 수업은 없을까?"
    ):
        print(chunk, end="")
