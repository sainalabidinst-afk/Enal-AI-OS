FROM python:3.11-slim AS base

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

# Install Python dependencies first for layer caching
COPY pyproject.toml ./

RUN pip install --no-cache-dir . \
    && chown -R appuser:appuser /usr/local/lib/python3.11/site-packages

# Copy application source code
COPY backend/ ./backend/
COPY apps/ ./apps/
COPY sdk/ ./sdk/
COPY real_cases/ ./real_cases/
COPY backend/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Observability / logging configuration
ENV LOG_FORMAT=json \
    LOG_LEVEL=INFO \
    LOGGING_PROVIDER=console

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Start application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
