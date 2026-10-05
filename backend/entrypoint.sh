#!/bin/bash
set -e

# Create workspace directories for memory layer
mkdir -p /app/workspace/memory/knowledge

# Try to chown, ignore if not permitted (tmpfs restrictions)
chown -R appuser:appuser /app/workspace 2>/dev/null || true

# Execute the main command
exec "$@"