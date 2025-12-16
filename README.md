# 📦 Task Tracker API

A Python-based API to manage and track tasks with Docker support for development and production environments.

## Requirements

- Docker
- Docker Compose
- make

## Setup

Create a `.env.dev` file in the project root with your configuration:

```env.dev
# App Info
APP_NAME=Website Tracker API
DEBUG=false
ENVIRONMENT=development

# CORS
ALLOWED_ORIGINS=["*"]

# Rate Limiting
RATE_LIMIT_REQUESTS=5
RATE_LIMIT_WINDOW=60

# Email Configuration
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_email_password
SMTP_SERVER=smtp.example.com
SMTP_PORT=587

# Slack Webhook
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url

# Logs
LOG_LEVEL=DEBUG

# Token
TOKEN="mytoken"
```

## Available Commands

Use `make help` to see all commands with detailed descriptions.

### Development

```bash
make build-dev    # Build development Docker image
make up-dev       # Start development server on port 8000
make down-dev     # Stop development server
make logs-dev     # View development logs
make test         # Run tests with pytest
```

### Production

```bash
make up-prod      # Start production environment
make down-prod    # Stop production environment  
make logs-prod    # View production logs
```

### Help

```bash
make help         # Show all available commands with descriptions
```

## Quick Start

### 1. Setup Environment

```bash
# Create .env file with your configuration (see Setup section above)
cp .env.example .env  # Edit with your values
```

### 2. Development Environment

```bash
# Start development server
make up-dev

# Server will be available at http://localhost:8000
# Hot reload enabled for development
```

### 3. Production Environment

```bash
# Start production server
make up-prod

# Stop production server
make down-prod
```

### 4. Running Tests

```bash
make test
```

## Project Structure

```
.
├── app/                      # Application code
├── tests/                    # Test files
├── docker-compose.dev.yaml   # Development configuration
├── docker-compose.prod.yaml  # Production configuration
├── Makefile                  # Task automation
└── README.md                 # This file
```

## Notes

- Development environment runs with hot reload enabled
- Production environment runs in detached mode with optimized settings
- Use `make help` to see all available commands with descriptions
