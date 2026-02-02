<h1 align="center" id="header">
  Task Tracker API - Python FastAPI Application
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions">
</p>

<p align="center">
  Professional task management API built with FastAPI, featuring email notifications, Slack integration, rate limiting, and containerized deployment.
</p>

---

<h2 id="stack">
  Tech Stack
</h2>

<p>
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Python-Dark.svg" width="48" title="Python"> 
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/FastAPI.svg" width="48" title="FastAPI">
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Docker.svg" width="48" title="Docker">
<img src="https://github.com/tandpfun/skill-icons/blob/main/icons/Grafana-Dark.svg" width="48" title="Grafana">
</p>

### Core Technologies

- **Python 3.11+** - Modern Python with latest features
- **FastAPI** - High-performance async web framework
- **Docker** - Containerized deployment
- **Pytest** - Comprehensive testing framework

### Features & Integrations

- **CORS Support** - Configurable cross-origin resource sharing
- **Rate Limiting** - API endpoint protection and request throttling
- **Email Notifications** - SMTP integration with configurable providers
- **Slack Webhooks** - Real-time notifications to Slack channels
- **Token Authentication** - Secure API access control
- **Environment-based Configuration** - Separate dev/prod settings
- **Logging** - Configurable log levels and monitoring
- **Hot Reload** - Development mode with automatic code reloading

---

<h2 id="prerequisites">
  Prerequisites
</h2>

Before starting, ensure you have the following installed:

- [Docker](https://www.docker.com/) - Container platform
- [Docker Compose](https://docs.docker.com/compose/) - Multi-container orchestration
- [Make](https://www.gnu.org/software/make/) - Build automation
- [Git](https://git-scm.com/) - Version control

> Optional: [Python 3.11+](https://www.python.org/) if you prefer running the app without Docker.

---

<h2 id="installation">
  Installation & Setup
</h2>

### 1. Clone the Repository

```bash
git clone https://github.com/Victor-Zarzar/task-tracker-api
cd task-tracker-api
```

### 2. Open in your editor

```bash
zed .   # Zed Editor
```

### 3. Environment Configuration

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env.dev
```

Then edit `.env.dev` with your actual values:

```env
# App Info
APP_NAME=Task Tracker API
DEBUG=false
ENVIRONMENT=development

# CORS
ALLOWED_ORIGINS=["*"]

# Rate Limiting
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW=60

# Email Configuration
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Slack Webhook
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url

# Logs
LOG_LEVEL=DEBUG

# Token
TOKEN=your_secure_token_here
```

**Key configurations needed:**

- **SMTP**: Email account and app password for notifications
- **Slack**: [Webhook URL](https://api.slack.com/messaging/webhooks) for Slack integration
- **Token**: Secure authentication token for API access

> **Important:** Never commit your `.env.dev` or `.env.prod` files to version control. They should be in `.gitignore`.

### 4. Build Development Environment

```bash
make build-dev
```

---

<h2 id="usage">
  Usage
</h2>

### Available Commands

View all available Make commands:

```bash
make help
```

### Local Development

Start the development server (port 8000):

```bash
make up-dev
```

Access the API at:

- **API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### Docker Deployment

#### Development Commands

```bash
make gen-secret   # Generate a new token
make build-dev    # Build development Docker image
make up-dev       # Start development server with hot reload
make down-dev     # Stop development server
make logs-dev     # View development logs in real-time
make test         # Run tests with pytest
make format       # Format code with Ruff
make lint         # Lint code with pylint
```

#### Production Commands

```bash
make up-prod      # Start production server
make down-prod    # Stop production server
make logs-prod    # View production logs
```

#### View Logs

```bash
make logs-dev     # Development logs
make logs-prod    # Production logs
```

Or directly with Docker:

```bash
docker logs -f task-tracker-api-dev
docker logs -f task-tracker-api-prod
```

---

<h2 id="makefile-commands">
  Makefile Commands Reference
</h2>

| Command           | Description                                   |
| ----------------- | --------------------------------------------- |
| `make build-dev`  | Build development Docker image                |
| `make up-dev`     | Start development server with hot reload      |
| `make down-dev`   | Stop and remove development containers        |
| `make logs-dev`   | Display development logs in real-time         |
| `make up-prod`    | Start production server (detached mode)       |
| `make down-prod`  | Stop and remove production containers         |
| `make logs-prod`  | Display production logs in real-time          |
| `make test`       | Run automated tests with pytest               |
| `make format`     | Format code with Ruff                         |
| `make lint`       | Lint code with pylint                         |
| `make gen-secret` | Generate a new token                          |
| `make help`       | Show all available commands with descriptions |

```bash
make test
```

Or manually with Docker:

```bash
docker-compose -f docker-compose.dev.yaml exec web pytest
```

### API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

<h2 id="project-structure">
  Project Structure
</h2>

```
task-tracker-api/
├── app/                        # Application code
│   ├── main.py                 # FastAPI application entry point
│   ├── routers/                # API route handlers
│   ├── models/                 # Data models
│   ├── services/               # Business logic
│   └── utils/                  # Utility functions
├── tests/                      # Test files
│   ├── test_api.py             # API endpoint tests
│   └── test_services.py        # Service layer tests
├── docker-compose.dev.yaml     # Development configuration
├── docker-compose.prod.yaml    # Production configuration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .env.dev                    # Development environment (not in git)
├── .env.prod                   # Production environment (not in git)
├── pyproject.toml              # Python project configuration
├── Makefile                    # Build automation
└── README.md                   # This file
```

---

<h2 id="code-quality">
  Code Quality & Formatting
</h2>

### Ruff Configuration

This project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and code formatting. The configuration is defined in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP"]
ignore = ["E501"]
fixable = ["ALL"]
unfixable = []
```

**Configuration details:**

- **Line length**: 88 characters (Black compatible)
- **Target version**: Python 3.12
- **Quote style**: Double quotes for strings
- **Linting rules**:
  - `E`, `W` - pycodestyle errors and warnings
  - `F` - Pyflakes
  - `I` - isort (import sorting)
  - `B` - flake8-bugbear
  - `UP` - pyupgrade (modern Python syntax)
- **Ignored rules**: `E501` (line too long)

### Running Code Quality Tools

All code quality tools run inside the Docker container:

```bash
# Format code with Ruff
make format

# Lint code with pylint
make lint
```

Or directly with Docker Compose:

```bash
# Format code
docker compose -f docker-compose.dev.yaml exec web ruff format app

# Lint code
docker compose -f docker-compose.dev.yaml exec web pylint app
```

---

<h2 id="api-endpoints">
  API Endpoints
</h2>

### Authentication

All endpoints require a valid token in the `Authorization` header:

```bash
Authorization: Bearer your_token_here
```

---

<h2 id="deployment">
   Deployment
</h2>

### Docker Production

Build and run the production container:

```bash
# Start production environment
make up-prod

# Check logs
make logs-prod

# Stop when needed
make down-prod
```

---

<h2 id="contributing">
  Contributing
</h2>

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guide
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

**Email notifications not working:**

- Ensure SMTP credentials are correct
- For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833)
- Check firewall settings for SMTP port

---

<h2 id="license">
  License
</h2>

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<h2 id="contact">
  Contact
</h2>

Victor Zarzar - [@Victor-Zarzar](https://github.com/Victor-Zarzar)

Project Link: [https://github.com/Victor-Zarzar/task-tracker-api](https://github.com/Victor-Zarzar/task-tracker-api)

---

<p align="center">
  Made with by Victor Zarzar
</p>
