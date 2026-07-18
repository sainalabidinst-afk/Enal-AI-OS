#!/bin/bash
set -e

echo "Waiting for dependencies..."

wait_for() {
  local host=$1
  local port=$2
  local timeout=${3:-30}
  local start=$(date +%s)
  while ! nc -z "$host" "$port" >/dev/null 2>&1; do
    now=$(date +%s)
    if (( now - start > timeout )); then
      echo "Timed out waiting for $host:$port"
      exit 1
    fi
    sleep 1
  done
  echo "$host:$port is ready"
}

wait_for "${DATABASE_HOST:-postgres}" "${DATABASE_PORT:-5432}" 60
wait_for "${REDIS_HOST:-redis}" "${REDIS_PORT:-6379}" 30
wait_for "${QDRANT_HOST:-qdrant}" "${QDRANT_PORT:-6333}" 30
wait_for "${OLLAMA_HOST:-ollama}" "${OLLAMA_PORT:-11434}" 30

echo "All dependencies ready. Starting backend..."
exec "$@"
