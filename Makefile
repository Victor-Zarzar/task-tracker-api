# Makefile Task Tracker API
DOCKER_IMAGE_NAME = task-tracker-api
DOCKER_CONTAINER_NAME = tracker-api-container
PORT = 8000
PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python
UVICORN = $(VENV)/bin/uvicorn
PROD_COMPOSE = docker-compose.prod.yaml

.PHONY: all setup install run stop clean docker-build docker-run docker-stop docker-clean help

all: help

setup:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created."

install: setup
	@echo "Installing dependencies..."
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed."

up-dev:
	@if [ ! -x "$(UVICORN)" ]; then \
		echo "❌ Dependencies not installed. Run 'make install' before starting the server."; \
		exit 1; \
	fi
	@echo "Starting server on port $(PORT)..."
	$(UVICORN) app.main:app --host 0.0.0.0 --port $(PORT) --reload

stop:
	@echo "Stopping server..."
	@-pkill -f "uvicorn main:app"
	@echo "Server stopped."

clean:
	@echo "Cleaning local environment..."
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf .pytest_cache
	@echo "Stopping and removing Docker Compose containers..."
	docker compose -f $(PROD_COMPOSE) down
	@echo "Environment cleaned."

up-prod:
	@echo "Subindo ambiente de produção com Docker Compose..."
	docker compose -f $(PROD_COMPOSE) up -d --build

down-prod:
	@echo "Parando ambiente de produção..."
	docker compose -f $(PROD_COMPOSE) down

logs-prod:
	@echo "Logs do ambiente de produção..."
	docker compose -f $(PROD_COMPOSE) logs -f	

docker-build:
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMAGE_NAME) .
	@echo "Docker image built."

docker-run:
	@echo "Starting Docker container on port $(PORT)..."
	docker run -d --name $(DOCKER_CONTAINER_NAME) -p $(PORT):$(PORT) $(DOCKER_IMAGE_NAME)
	@echo "Docker container started."

docker-stop:
	@echo "Stopping Docker container..."
	docker stop $(DOCKER_CONTAINER_NAME)
	docker rm $(DOCKER_CONTAINER_NAME)
	@echo "Docker container stopped and removed."

docker-clean: docker-stop
	@echo "Removing Docker image..."
	docker rmi $(DOCKER_IMAGE_NAME)
	@echo "Docker image removed."

docker-logs:
	@echo "Showing container logs..."
	docker logs -f $(DOCKER_CONTAINER_NAME)

docker-shell:
	@echo "Accessing container shell..."
	docker exec -it $(DOCKER_CONTAINER_NAME) /bin/bash

help:
	@echo ""
	@echo "📦 Tracker API Server Makefile"
	@echo "──────────────────────────────────────────────"
	@echo "🛠️  Development Commands:"
	@echo "  make setup            ➜ Create virtual environment"
	@echo "  make install          ➜ Install dependencies"
	@echo "  make up               ➜ Run local server (dev)"
	@echo "  make stop             ➜ Stop local server"
	@echo "  make test             ➜ Run tests with pytest"
	@echo "  make clean            ➜ Clean local environment and containers"
	@echo ""
    @echo "🚀 Comandos de Produção:"
	@echo "  make up-prod          ➜ Subir ambiente de produção com Docker Compose"
	@echo "  make down-prod        ➜ Parar ambiente de produção"
	@echo "  make logs-prod        ➜ Exibir logs da produção"
	@echo ""
	@echo "🐳 Docker Commands (manual usage):"
	@echo "  make docker-build     ➜ Build Docker image manually"
	@echo "  make docker-run       ➜ Run Docker container manually"
	@echo "  make docker-stop      ➜ Stop and remove manual Docker container"
	@echo "  make docker-clean     ➜ Remove Docker image"
	@echo "  make docker-logs      ➜ Show logs from manual Docker container"
	@echo "  make docker-shell     ➜ Access shell inside manual Docker container"
	@echo ""
	@echo "ℹ️  Tip: Always run 'make install' before 'make up'"
