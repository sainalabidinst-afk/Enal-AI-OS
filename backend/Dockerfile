FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

# Copy the monorepo with the runtime ownership already applied.
COPY --chown=appuser:appuser . .

# Ensure appuser owns all copied files and create writable workspace
RUN mkdir -p /app/workspace \
    && chown appuser:appuser /app/workspace

# Set PYTHONPATH so backend, apps, workspace, plugins are all resolvable from /app
ENV PYTHONPATH=/app

# Install backend package from monorepo root
RUN pip install --no-cache-dir -e . && pip install --no-cache-dir PyJWT && chown -R appuser:appuser /usr/local/lib/python3.11/site-packages

USER appuser

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
