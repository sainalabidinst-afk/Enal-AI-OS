Write-Host "================================"
Write-Host "   Enal AI OS Setup Script"
Write-Host "================================"
Write-Host ""

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example"
} else {
    Write-Host ".env already exists, skipping"
}

Write-Host ""
Write-Host "Starting Docker services..."
docker-compose up -d postgres redis qdrant ollama

Write-Host ""
Write-Host "Waiting for services to be ready..."
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Installing Python dependencies..."
Set-Location backend
pip install poetry
poetry install
Set-Location ..

Write-Host ""
Write-Host "Installing Node dependencies..."
Set-Location frontend
npm install
Set-Location ..

Write-Host ""
Write-Host "================================"
Write-Host "   Setup Complete!"
Write-Host "================================"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit .env and add your API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)"
Write-Host "2. Start backend:  cd backend; poetry run uvicorn backend.app.main:app --reload"
Write-Host "3. Start frontend: cd frontend; npm run dev"
Write-Host "4. Open http://localhost:3000"
Write-Host ""
Write-Host "Or use Docker Compose for all services:"
Write-Host "  docker-compose up -d"
