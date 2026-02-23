# Dockerfile
FROM python:3.14.3-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY requirements.txt .
RUN uv venv && uv pip install -r requirements.txt

COPY src/ ./src/

CMD ["uv", "run", "python", "-u", "src/main.py"]
