# Makefile Task Tracker API
PROJECT_NAME = Task Tracker API
VERSION = 1.0.0
PORT = 8000
DEV_COMPOSE = docker-compose.dev.yaml
PROD_COMPOSE = docker-compose.prod.yaml

gen-secret:
	openssl rand -hex 64

build-dev:
	docker compose -f $(DEV_COMPOSE) build

up-dev:
	docker compose -f $(DEV_COMPOSE) up

down-dev:
	docker compose -f $(DEV_COMPOSE) down

logs-dev:
	docker compose -f $(DEV_COMPOSE) logs -f

test:
	docker compose -f $(DEV_COMPOSE) exec web pytest

clean:
	docker compose -f $(DEV_COMPOSE) down -v --remove-orphans 2>/dev/null || true
	docker compose -f $(PROD_COMPOSE) down -v --remove-orphans 2>/dev/null || true
	docker image prune -af || true
	docker volume prune -f || true
	docker builder prune -f || true
	find . -name "_pycache_" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -type f -delete 2>/dev/null || true
	sudo rm -rf .pytest_cache .coverage htmlcov 2>/dev/null .ruff_cache || true

build-prod:
	docker compose -f $(PROD_COMPOSE) build

up-prod:
	docker compose -f $(PROD_COMPOSE) up -d --build

down-prod:
	docker compose -f $(PROD_COMPOSE) down

logs-prod:
	docker compose -f $(PROD_COMPOSE) logs -f

format:
	docker compose -f $(DEV_COMPOSE) exec web ruff format app

lint:
	docker compose -f $(DEV_COMPOSE) exec web pylint app

help:
	@echo ""
	@echo "$(PROJECT_NAME) ($(VERSION))"
	@echo "──────────────────────────────────────────────"
	@echo "Development Commands:"
	@echo "  make build-dev  ➜ Build image Docker (development)"
	@echo "  make up-dev     ➜ Run local server (development)"
	@echo "  make stop       ➜ Stop local server"
	@echo "  make test       ➜ Run tests with pytest"
	@echo "  make clean      ➜ Clean local environment and containers"
	@echo "  make gen-secret ➜ Generate a new token"
	@echo "  make lint       ➜ Lint code with pylint"
	@echo "  make format     ➜ Format code with ruff"
	@echo ""
	@echo "Production Commands:"
	@echo "  make build-prod ➜ Build image Docker (prod)"
	@echo "  make up-prod    ➜ Start production environment with Docker Compose"
	@echo "  make down-prod  ➜ Stop production environment"
	@echo "  make logs-prod  ➜ Show production logs"
	@echo ""
