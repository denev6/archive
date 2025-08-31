FROM python:3.10-slim

RUN apt-get update && apt-get install -y curl --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN pip install pipx && \
    pipx ensurepath && \
    pipx install uv

WORKDIR /app
COPY . .

ENV PATH="/root/.local/bin:$PATH"
RUN uv sync

ENV PATH="/app/.venv/bin:$PATH"
RUN uv run python load_model.py

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8001"]