# Docker Compose Setup for MealMind

This document explains how to use the Docker Compose configuration to orchestrate all MealMind services.

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git repository cloned locally

### Starting All Services
```bash
# Start all services in detached mode
docker compose up -d

# Check service status
docker compose ps

# View logs for all services
docker compose logs

# View logs for specific service
docker compose logs api
```

### Stopping All Services
```bash
# Stop and remove all containers
docker compose down

# Stop and remove containers, networks, and volumes
docker compose down -v
```

## Services Overview

### 1. Database (PostgreSQL)
- **Image**: `postgres:15-alpine`
- **Port**: `54322:5432`
- **Status**: ✅ Working
- **Health Check**: Included
- **Access**: `postgres://postgres:postgres@localhost:54322/postgres`
- **Tables**: 7 tables (recipes, categories, brands, ingredients, recipe_ingredients, meal_plans, alembic_version)
- **Migrations**: Managed by Alembic (current: 6942d77a42e3)

### 2. FastAPI Backend
- **Build**: Custom from `./apps/api/Dockerfile`
- **Port**: `8000:8000`
- **Status**: ✅ Working
- **Health Check**: `GET /health`
- **Endpoints**:
  - `GET /` - Welcome message
  - `GET /health` - Health check
- **ORM**: SQLAlchemy 2.0+ with Alembic migrations

### 3. Supabase REST API (PostgREST)
- **Image**: `postgrest/postgrest:v12.2.4`
- **Port**: `54321:3000`
- **Status**: ✅ Working
- **Purpose**: Auto-generated REST API from database schema
- **Usage**: Complements FastAPI for simple CRUD operations

### 4. Supabase Postgres Meta
- **Image**: `supabase/postgres-meta:v0.75.0`
- **Port**: Internal only (8080)
- **Status**: ✅ Working
- **Purpose**: Database metadata API for Supabase Studio

### 5. Supabase Studio
- **Image**: `supabase/studio:20231123-64a766a`
- **Port**: `54323:3000`
- **Status**: ✅ Working
- **Purpose**: Visual database management UI
- **Access**: http://localhost:54323
- **Features**: Browse tables, run SQL queries, view relationships

### 6. Email Service (Inbucket)
- **Image**: `inbucket/inbucket:stable`
- **Ports**: 
  - `54324:9000` - Web interface
  - `54325:9025` - SMTP
  - `54326:9110` - POP3
- **Status**: ✅ Working
- **Purpose**: Email testing and debugging (for Phase 4)

### 7. Frontend (SvelteKit)
- **Build**: Custom from `./apps/frontend/Dockerfile`
- **Port**: `3000:3000`
- **Status**: ✅ Running
- **Purpose**: User interface for MealMind application

## Network Configuration

All services communicate through a custom Docker network called `meal-mind-network`. This enables:

- Service discovery by name (e.g., `api`, `db`, `supabase-rest`)
- Secure inter-container communication
- Isolation from other Docker networks

## Environment Variables

### API Service
- `SUPABASE_URL=http://supabase-rest:3000`
- `DATABASE_URL=postgres://postgres:postgres@db:5432/postgres`

### Frontend Service (when enabled)
- `PUBLIC_SUPABASE_URL=http://localhost:54321`
- `API_URL=http://api:8000`

## Volume Persistence

- **Database Data**: Stored in `db_data` volume
- **Data Location**: Managed by Docker, persists between container restarts

## Development Workflow

### Building and Testing Changes

```bash
# Rebuild specific service after code changes
docker compose build api
docker compose up -d api

# Rebuild all services
docker compose build
docker compose up -d

# View real-time logs
docker compose logs -f api
```

### Accessing Services

- **API**: http://localhost:8000
- **Database**: localhost:54322 (PostgreSQL client)
- **Supabase Studio**: http://localhost:54323 (Visual database manager)
- **Supabase REST API**: http://localhost:54321 (Auto-generated REST endpoints)
- **Email Web UI**: http://localhost:54324
- **Frontend**: http://localhost:3000

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's using a port
   lsof -i :8000
   
   # Stop conflicting services
   sudo service postgresql stop  # if using local PostgreSQL
   ```

2. **Build Failures**
   ```bash
   # Clean rebuild
   docker compose down -v
   docker compose build --no-cache
   docker compose up -d
   ```

3. **Service Health Checks**
   ```bash
   # Check service health
   docker compose ps
   
   # Inspect specific container
   docker compose exec api python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
   ```

### Logs and Debugging

```bash
# View all logs
docker compose logs

# Follow logs for specific service
docker compose logs -f api

# Execute commands in running container
docker compose exec api bash
docker compose exec db psql -U postgres
```

## Next Steps

### To Complete Supabase Integration:
- Configure PostgREST roles and permissions
- Add authentication service (optional)
- Configure storage service (optional)

## Production Considerations

- Use environment-specific configuration files
- Implement proper secrets management
- Add monitoring and logging solutions
- Configure reverse proxy (nginx/traefik)
- Set up automated backups for database volumes