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

### 2. FastAPI Backend
- **Build**: Custom from `./apps/api/Dockerfile`
- **Port**: `8000:8000`
- **Status**: ✅ Working
- **Health Check**: `GET /health`
- **Endpoints**:
  - `GET /` - Welcome message
  - `GET /health` - Health check

### 3. Supabase REST API (PostgREST)
- **Image**: `postgrest/postgrest:v12.2.4`
- **Port**: `54321:3000`
- **Status**: ⚠️ Needs database schema setup
- **Purpose**: Auto-generated REST API from database schema

### 4. Email Service (Inbucket)
- **Image**: `inbucket/inbucket:stable`
- **Ports**: 
  - `54324:9000` - Web interface
  - `54325:9025` - SMTP
  - `54326:9110` - POP3
- **Status**: ✅ Working
- **Purpose**: Email testing and debugging

### 5. Frontend (SvelteKit) - Currently Disabled
- **Build**: Custom from `./apps/frontend/Dockerfile`
- **Port**: `3000:3000`
- **Status**: ⏸️ Build optimization needed
- **Note**: Commented out until build issues are resolved

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
- **Email Web UI**: http://localhost:54324
- **Supabase REST**: http://localhost:54321 (when working)

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

### To Enable Frontend Service:
1. Fix the Node.js build process in the Dockerfile
2. Uncomment the frontend service in docker-compose.yml
3. Test the build with `docker compose build frontend`

### To Complete Supabase Setup:
1. Add database migrations for Supabase schema
2. Configure PostgREST with proper database roles
3. Add additional Supabase services (Auth, Storage, etc.)

## Production Considerations

- Use environment-specific configuration files
- Implement proper secrets management
- Add monitoring and logging solutions
- Configure reverse proxy (nginx/traefik)
- Set up automated backups for database volumes