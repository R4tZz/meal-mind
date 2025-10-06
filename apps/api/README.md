# MealMind API

FastAPI backend service for the MealMind application, providing meal planning and nutrition management functionality.

## Features

- RESTful API built with FastAPI
- PostgreSQL database with Alembic migrations
- Comprehensive test suite with 85%+ coverage
- Health check endpoint for monitoring
- Dockerized deployment with uv package management
- Python 3.12+ support

## Database

This API uses PostgreSQL with SQLAlchemy ORM and Alembic for migrations.

### Schema

The database consists of 6 main tables:

- **recipes** - Recipe metadata (name, servings, timestamps)
- **categories** - Ingredient categories (e.g., Dairy, Vegetables)
- **brands** - Product brands (e.g., Organic Valley)
- **ingredients** - Individual ingredients with optional category/brand
- **recipe_ingredients** - Junction table linking recipes to ingredients with quantities
- **meal_plans** - Planned meals with date and meal type

### Migrations

Run migrations using Alembic:

```bash
# Upgrade to latest version
uv run alembic upgrade head

# Create a new migration
uv run alembic revision --autogenerate -m "description"

# Downgrade one version
uv run alembic downgrade -1
```

For detailed migration setup, see [DOCKER_SETUP.md](../../DOCKER_SETUP.md).

## Testing

The project includes a comprehensive test suite covering database migrations, constraints, relationships, and cascade behaviors.

### Running Tests

```bash
# Run all integration tests
uv run pytest tests/integration/

# Run with verbose output
uv run pytest tests/integration/ -v

# Run with coverage report
uv run pytest --cov=. --cov-report=html tests/integration/

# Run specific test file
uv run pytest tests/integration/test_migrations.py
```

### Test Organization

- **tests/integration/** - Database integration tests
- **tests/unit/** - Unit tests (future)
- **tests/e2e/** - End-to-end tests (future)

For complete testing documentation, see [tests/README.md](tests/README.md).

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
├── alembic/          # Database migrations
│   ├── versions/     # Migration scripts
│   └── env.py        # Alembic environment configuration
├── core/             # Core configuration
│   └── config.py     # Database and app configuration
├── models/           # SQLAlchemy models
│   ├── recipe.py
│   ├── ingredient.py
│   ├── category.py
│   ├── brand.py
│   ├── recipe_ingredient.py
│   ├── meal_plan.py
│   └── enums.py
├── tests/            # Test suite (see tests/README.md)
│   ├── integration/  # Database integration tests
│   ├── unit/         # Unit tests
│   └── e2e/          # End-to-end tests
├── main.py           # FastAPI application
├── pyproject.toml    # Project configuration and dependencies
├── uv.lock           # Locked dependencies
├── Dockerfile        # Docker configuration
├── .dockerignore     # Docker ignore rules
└── README.md         # This file
```
