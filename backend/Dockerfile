FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction

COPY backend /app/backend
COPY apps /app/apps
COPY plugins /app/plugins
COPY golden /app/golden
COPY real_cases /app/real_cases
COPY benchmarks /app/benchmarks

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
