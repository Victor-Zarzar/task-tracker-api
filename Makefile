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

.PHONY: all setup install up-dev stop clean up-prod down-prod logs-prod docker-build docker-run docker-stop docker-clean docker-logs docker-shell test help

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
	@-pkill -f "uvicorn app.main:app"
	@echo "Server stopped."

test:
	@echo "Running tests..."
	$(VENV)/bin/pytest
	@echo "Tests completed."

clean:
	@echo "Cleaning local environment..."
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf .pytest_cache
	@echo "Stopping and removing Docker Compose containers..."
	docker compose -f $(PROD_COMPOSE) down 2>/dev/null || true
	@echo "Environment cleaned."

up-prod:
	@echo "🚀 Starting production environment with Docker Compose..."
	docker compose -f $(PROD_COMPOSE) up -d --build

down-prod:
	@echo "🛑 Stopping production environment..."
	docker compose -f $(PROD_COMPOSE) down

logs-prod:
	@echo "📋 Production environment logs..."
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
	docker stop $(DOCKER_CONTAINER_NAME) 2>/dev/null || true
	docker rm $(DOCKER_CONTAINER_NAME) 2>/dev/null || true
	@echo "Docker container stopped and removed."

docker-clean: docker-stop
	@echo "Removing Docker image..."
	docker rmi $(DOCKER_IMAGE_NAME) 2>/dev/null || true
	@echo "Docker image removed."

docker-logs:
	@echo "Showing container logs..."
	docker logs -f $(DOCKER_CONTAINER_NAME)

docker-shell:
	@echo "Accessing container shell..."
	docker exec -it $(DOCKER_CONTAINER_NAME) /bin/bash

help:
	@echo ""
	@echo "📦 Task Tracker API - Makefile Commands"
	@echo "──────────────────────────────────────────────"
	@echo "🛠️  Development Commands:"
	@echo "  make setup     ➜ Create virtual environment"
	@echo "  make install   ➜ Install dependencies"
	@echo "  make up-dev    ➜ Run local server (development)"
	@echo "  make stop      ➜ Stop local server"
	@echo "  make test      ➜ Run tests with pytest"
	@echo "  make clean     ➜ Clean local environment and containers"
	@echo ""
	@echo "🚀 Production Commands:"
	@echo "  make up-prod   ➜ Start production environment with Docker Compose"
	@echo "  make down-prod ➜ Stop production environment"
	@echo "  make logs-prod ➜ Show production logs"
	@echo ""
	@echo "🐳 Docker Commands (manual usage):"
	@echo "  make docker-build ➜ Build Docker image manually"
	@echo "  make docker-run   ➜ Run Docker container manually"
	@echo "  make docker-stop  ➜ Stop and remove manual Docker container"
	@echo "  make docker-clean ➜ Remove Docker image"
	@echo "  make docker-logs  ➜ Show logs from manual Docker container"
	@echo "  make docker-shell ➜ Access shell inside manual Docker container"
	@echo ""
	@echo "ℹ️  Tip: Always run 'make install' before 'make up-dev'"
	@echo ""