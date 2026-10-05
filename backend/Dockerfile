FROM python:3.11-slim AS base

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

# Install Python dependencies first for layer caching
# Copy only pyproject.toml to leverage Docker layer cache
COPY pyproject.toml ./
COPY setup.py setup.cfg ./
COPY backend/ ./backend/
COPY apps/ ./apps/
COPY sdk/ ./sdk/

RUN pip install --no-cache-dir --no-deps -e . \
    && pip install --no-cache-dir PyJWT uvicorn[standard] \
    && chown -R appuser:appuser /usr/local/lib/python3.11/site-packages

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
