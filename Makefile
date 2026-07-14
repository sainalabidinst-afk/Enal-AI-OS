.PHONY: help up down logs backend frontend test clean

help:
	@echo "Enal AI OS - Makefile"
	@echo ""
	@echo "make up          - Start all services"
	@echo "make down        - Stop all services"
	@echo "make logs        - Show logs"
	@echo "make backend     - Run backend dev server"
	@echo "make frontend    - Run frontend dev server"
	@echo "make test        - Run tests"
	@echo "make clean       - Remove containers and volumes"

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

backend:
	cd backend && poetry install && uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm install && npm run dev

test:
	cd backend && pytest

clean:
	docker-compose down -v
	rm -rf backend/.venv frontend/node_modules
