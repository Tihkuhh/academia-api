FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    netcat-openbsd \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
ENV PYTHONPATH=/app

# O comando de execução real será sobrescrito pelo docker-compose.yml
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000"]