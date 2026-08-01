.PHONY: help up down logs backend frontend test clean benchmark-network gate0 gate01 release-readiness

help:
	@echo "Enal AI OS - Makefile"
	@echo ""
	@echo "make up                - Start all services"
	@echo "make down              - Stop all services"
	@echo "make logs              - Show logs"
	@echo "make backend           - Run backend dev server"
	@echo "make frontend          - Run frontend dev server"
	@echo "make test              - Run tests"
	@echo "make benchmark-network - Run Network Engineer benchmark"
	@echo "make gate0             - Run Gate 0 certification (infrastructure)"
	@echo "make gate01            - Run Gate 0/1/2 certification"
	@echo "make release-readiness - Show release readiness dashboard"
	@echo "make clean             - Remove containers and volumes"

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

backend:
	pip install -e ".[dev]" && uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm install && npm run dev

test:
	cd backend && pytest

benchmark-network:
	cd benchmarks && python network_engineer_benchmark.py

gate0:
	cd scripts && python gate0_validate.py

gate01:
	cd scripts && python gate0_validate.py

release-readiness:
	cd scripts && python release_readiness.py

clean:
	docker-compose down -v
	rm -rf backend/.venv frontend/node_modules
