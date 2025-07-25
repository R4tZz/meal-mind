# MealMind API

FastAPI backend service for the MealMind application, providing meal planning and nutrition management functionality.

## Features

- RESTful API built with FastAPI
- Health check endpoint for monitoring
- Dockerized deployment with uv package management
- Python 3.12+ support

## Quick Start

### Local Development

1. Install dependencies using uv:
```bash
uv sync
```

2. Run the development server:
```bash
uv run python main.py
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t meal-mind-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 meal-mind-api
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Development

This project uses:
- **FastAPI** - Modern, fast web framework for building APIs
- **uv** - Fast Python package manager
- **Uvicorn** - ASGI server implementation
- **Docker** - Containerization platform

## Project Structure

```
apps/api/
├── main.py           # FastAPI application
├── pyproject.toml    # Project configuration and dependencies
├── uv.lock          # Locked dependencies
├── Dockerfile       # Docker configuration
├── .dockerignore    # Docker ignore rules
└── README.md        # This file
```