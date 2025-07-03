.PHONY: help install test run clean docker-build docker-run

help: ## Show this help message
	@echo "GeoMask - AI-powered photo privacy protection"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest pytest-asyncio black flake8 mypy

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=app --cov-report=html

lint: ## Run linting
	black app/ tests/
	flake8 app/ tests/
	mypy app/

format: ## Format code
	black app/ tests/

run: ## Run the application
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-frontend: ## Run frontend development server
	cd frontend && npm start

run-backend: ## Run backend only
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

docker-build: ## Build Docker image
	docker build -t geomask .

docker-run: ## Run with Docker
	docker run -p 8000:8000 geomask

docker-compose-up: ## Start with Docker Compose
	docker-compose up -d

docker-compose-down: ## Stop Docker Compose
	docker-compose down

setup: ## Initial setup
	mkdir -p uploads processed output temp logs
	cp env.example .env
	@echo "Please edit .env file with your API keys"

start: ## Start the application (backend + frontend)
	@echo "Starting GeoMask..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "Press Ctrl+C to stop"
	@bash scripts/start.sh 