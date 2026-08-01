FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser \
    && chown -R appuser:appuser /app

# Copy entire monorepo — preserves /app/backend, /app/apps, /app/workspace, /app/plugins
COPY . .

# Set PYTHONPATH so backend, apps, workspace, plugins are all resolvable from /app
ENV PYTHONPATH=/app

# Install backend package from monorepo root
RUN pip install --no-cache-dir -e .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
