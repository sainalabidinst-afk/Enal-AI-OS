#!/bin/bash
set -e

echo "================================"
echo "   Enal AI OS Setup Script"
echo "================================"
echo ""

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
else
    echo ".env already exists, skipping"
fi

echo ""
echo "Starting Docker services..."
docker-compose up -d postgres redis qdrant ollama

echo ""
echo "Waiting for services to be ready..."
sleep 5

echo ""
echo "Installing Python dependencies..."
cd backend
pip install poetry
poetry install
cd ..

echo ""
echo "Installing Node dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "================================"
echo "   Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)"
echo "2. Start backend:  cd backend && poetry run uvicorn backend.app.main:app --reload"
echo "3. Start frontend: cd frontend && npm run dev"
echo "4. Open http://localhost:3000"
echo ""
echo "Or use Docker Compose for all services:"
echo "  docker-compose up -d"
