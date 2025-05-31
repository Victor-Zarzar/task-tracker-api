# 📦 Task Tracker API

A Python-based API to manage and track tasks, supporting both local development and Docker-based production environments.

---

## ⚙️ Requirements

- Python 3.10+
- Docker
- Docker Compose
- make

---

## 🛠️ Makefile Commands

### 📦 Development

| Command           | Description                                       |
|-------------------|---------------------------------------------------|
| `make setup`      | Create a virtual environment                      |
| `make install`    | Install dependencies into the virtual environment |
| `make up-dev`     | Start local development server (Uvicorn + reload) |
| `make stop`       | Stop the local development server                 |
| `make test`       | Run tests with `pytest`                           |
| `make clean`      | Clean virtual environment and Docker containers   |

> 💡 Tip: Always run `make install` before `make up-dev`.

---

### 🚀 Production (Docker Compose)

| Command             | Description                                      |
|---------------------|--------------------------------------------------|
| `make up-prod`      | Start production environment with Docker Compose |
| `make down-prod`    | Stop production environment                      |
| `make logs-prod`    | Show logs for the production environment         |

---

### 🐳 Docker (Manual)

| Command               | Description                          |
|------------------------|--------------------------------------|
| `make docker-build`    | Build the Docker image               |
| `make docker-run`      | Run the Docker container             |
| `make docker-stop`     | Stop and remove the container        |
| `make docker-clean`    | Remove the Docker image              |
| `make docker-logs`     | Show container logs                  |
| `make docker-shell`    | Access container shell via bash      |

---

## 📂 Project Structure

.
├── app/ # Application code
├── tests/ # Tests
├── requirements.txt # Python dependencies
├── Dockerfile # Docker image instructions
├── docker-compose.prod.yaml # Production Compose file
├── Makefile # Task automation
└── README.md # Project documentation

---

## ▶️ Quickstart

### Local Development

```bash
make install     # Create virtualenv and install dependencies
make up-dev      # Start local server at http://localhost:8000