# Makefile Task Tracker API
DOCKER_IMAGE_NAME = task-tracker-api
DOCKER_CONTAINER_NAME = tracker-api-container
PORT = 8000
DEV_COMPOSE = docker-compose.dev.yaml
PROD_COMPOSE = docker-compose.prod.yaml

build-dev:
	@echo "Building development image dev..."
	docker compose -f $(DEV_COMPOSE) build

up-dev:
	@echo "Uploading development environment on port $(PORT)..."
	docker compose -f $(DEV_COMPOSE) up	

down-dev:
	@echo "Stopping server..."
	docker compose -f $(DEV_COMPOSE) down
	@echo "Server stopped."

logs-dev:
	@echo "Development environment logs..."
	docker compose -f $(DEV_COMPOSE) logs -f	

test:
	@echo "Running tests..."
	docker compose -f $(DEV_COMPOSE) exec web pytest
	@echo "Tests completed."

clean:
	@echo "Cleaning local environment..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache 2>/dev/null || true
	@echo "Stopping and removing Docker Compose containers..."
	@docker compose -f $(DEV_COMPOSE) down -v 2>/dev/null || true
	@docker compose -f $(PROD_COMPOSE) down -v 2>/dev/null || true
	@echo "Environment cleaned."

build-prod:
	@echo "Building development image prod..."
	docker compose -f $(PROD_COMPOSE) build	

up-prod:
	@echo "🚀 Starting production environment with Docker Compose..."
	docker compose -f $(PROD_COMPOSE) up -d --build

down-prod:
	@echo "🛑 Stopping production environment..."
	docker compose -f $(PROD_COMPOSE) down

logs-prod:
	@echo "📋 Production environment logs..."
	docker compose -f $(PROD_COMPOSE) logs -f

help:
	@echo ""
	@echo "📦 Task Tracker API - Makefile Commands"
	@echo "──────────────────────────────────────────────"
	@echo "🛠️  Development Commands:"
	@echo "  make build-dev  ➜ Build image Docker (development)"
	@echo "  make up-dev     ➜ Run local server (development)"
	@echo "  make stop       ➜ Stop local server"
	@echo "  make test       ➜ Run tests with pytest"
	@echo "  make clean      ➜ Clean local environment and containers"
	@echo ""
	@echo "🚀 Production Commands:"
	@echo "  make build-prod ➜ Build image Docker (prod)"
	@echo "  make up-prod    ➜ Start production environment with Docker Compose"
	@echo "  make down-prod  ➜ Stop production environment"
	@echo "  make logs-prod  ➜ Show production logs"
	@echo ""