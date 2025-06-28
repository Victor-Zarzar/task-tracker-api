# 📦 Task Tracker API

A Python-based API to manage and track tasks with Docker support for development and production environments.

## Requirements

- Docker
- Docker Compose
- make

## Available Commands

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

### Maintenance

```bash
make clean        # Clean environment and remove containers
make help         # Show all available commands
```

## Quick Start

### Development Environment

```bash
# Start development server
make up-dev

# Server will be available at http://localhost:8000
# Hot reload enabled for development
```

### Production Environment

```bash
# Start production server
make up-prod

# Stop production server
make down-prod
```

### Running Tests

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
├── Makefile                   # Task automation
└── README.md                 # This file
```

## Notes

- Development environment runs with hot reload enabled
- Production environment runs in detached mode with optimized settings
- Use `make help` to see all available commands with descriptions