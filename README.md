# MealMind 🍽️

**A personal web application that acts as a household assistant, streamlining meal planning, automating grocery list generation, and facilitating timely communication of shopping needs.**

## 🎯 Project Goal

MealMind helps busy households by:

- **Meal Planning**: Plan your weekly meals with ease
- **Grocery List Generation**: Automatically generate shopping lists from planned meals
- **Smart Notifications**: Get timely reminders for grocery shopping
- **Recipe Management**: Store and organize your favorite recipes

## 🛠️ Technology Stack

### Backend

- **FastAPI** (Python) - High-performance web framework
- **PostgreSQL** - Robust database via Supabase
- **uv** - Modern Python package manager
- **pytest** - Comprehensive testing

### Frontend

- **SvelteKit** (TypeScript) - Modern web framework
- **Tailwind CSS** - Utility-first styling
- **shadcn/svelte** - Beautiful UI components
- **Vitest** + **Playwright** - Unit and E2E testing

### Infrastructure

- **Docker** + **Docker Compose** - Containerization and orchestration
- **Nx** - Monorepo management and build system
- **GitHub Actions** - CI/CD pipeline
- **PostgreSQL 15** - Production-grade database
- **PostgREST** - Auto-generated REST API from database schema
- **Inbucket** - Email testing and debugging

## 🏗️ Architecture

```
User Browser ↔ SvelteKit Frontend (Port 3000) ↔ FastAPI Backend (Port 8000) ↔ PostgreSQL (Port 54322)
                                                          ↓
                                                  PostgREST (Port 54321)
```

The application runs as a containerized microservices architecture:

- **Frontend Container**: SvelteKit app serving the user interface
- **Backend Container**: FastAPI handling business logic and API endpoints
- **Database Container**: PostgreSQL 15 for data persistence
- **PostgREST Container**: Auto-generated REST API from database schema
- **Email Container**: Inbucket for email testing in development
- **Network**: All services communicate through `meal-mind-network`

### Current API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /db-test` - Database connection verification

## 🚀 Getting Started

### Prerequisites

- **Docker Desktop** - Container runtime (required)
- **Node.js** (v20+) - For local development (optional)
- **Python** (3.12+) - For local development (optional)

### Quick Start with Docker

The easiest way to get started is using Docker Compose, which will set up all services automatically:

1. **Clone the repository**

   ```bash
   git clone https://github.com/R4tZz/meal-mind.git
   cd meal-mind
   ```

2. **Start all services**

   ```bash
   docker compose up -d
   ```

   This will start:
   - PostgreSQL database (port 54322)
   - FastAPI backend (port 8000)
   - SvelteKit frontend (port 3000)
   - Supabase REST API/PostgREST (port 54321)
   - Email testing service/Inbucket (port 54324)

3. **Verify everything is running**

   ```bash
   docker compose ps
   ```

4. **Access the application**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Health Check**: http://localhost:8000/health
   - **Database Test**: http://localhost:8000/db-test
   - **Supabase REST**: http://localhost:54321
   - **Email Testing UI**: http://localhost:54324

### Stopping Services

```bash
# Stop all containers
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v
```

### Viewing Logs

```bash
# All services
docker compose logs

# Specific service
docker compose logs api
docker compose logs frontend
docker compose logs db

# Follow logs in real-time
docker compose logs -f api
```

## � Docker Services

The application uses Docker Compose to orchestrate multiple services:

| Service | Port | Description | Status |
|---------|------|-------------|--------|
| **frontend** | 3000 | SvelteKit web application | ✅ Running |
| **api** | 8000 | FastAPI backend service | ✅ Running |
| **db** | 54322 | PostgreSQL 15 database | ✅ Running |
| **supabase-rest** | 54321 | PostgREST API gateway | ✅ Running |
| **supabase-inbucket** | 54324 | Email testing UI | ✅ Running |

### Service Health

All services include health checks to ensure proper startup:
- **Database**: Checks PostgreSQL readiness
- **API**: Monitors `/health` endpoint
- **Frontend**: Verifies application response

### Environment Variables

**API Container:**
```env
SUPABASE_URL=http://supabase-rest:3000
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
```

**Frontend Container:**
```env
PUBLIC_SUPABASE_URL=http://localhost:54321
API_URL=http://api:8000
```

For more details, see [DOCKER_SETUP.md](DOCKER_SETUP.md)

## �📋 Development Workflow

This project follows **Scrum methodology** with GitHub Projects:

### Project Board Columns

- **Backlog** - All unassigned tasks
- **To Do (Sprint Backlog)** - Current sprint tasks
- **In Progress** - Active development
- **In Review/Testing** - Code review and testing
- **Done** - Completed tasks

### Definition of Done ✅

- Code is written and functional
- **Unit tests** are written and pass
- **Integration/API tests** (Backend) or **E2E tests** (Frontend) pass
- Code is reviewed and approved
- Code is merged to `main` branch
- Documentation is updated

## 🎯 Project Phases

### Phase 1: Foundation ⚙️

**Status: In Progress**

- [x] Nx monorepo setup
- [x] Docker containerization (API, Frontend, Database)
- [x] PostgreSQL database with health checks
- [x] FastAPI backend with basic endpoints
- [x] SvelteKit frontend with communication tests
- [x] Container networking and orchestration
- [ ] Testing infrastructure setup
- [ ] Initial test runners for frontend and backend

### Phase 2: Backend Development 🔧

**Status: Planned**

- Recipe management API
- Meal planning logic
- Grocery list generation
- Database schema & migrations

### Phase 3: Frontend Development 🎨

**Status: Planned**

- Recipe management UI
- Meal planning interface
- Grocery list display
- Responsive design

### Phase 4: Notifications 📧

**Status: Planned**

- Email notification system
- Automated scheduling
- Frontend triggers

### Phase 5: Deployment 🚀

**Status: Planned**

- Cloud deployment
- CI/CD pipeline
- Environment management

### Phase 6: Refinement ✨

**Status: Planned**

- User feedback integration
- Feature enhancements
- Performance optimization

## 🧪 Testing Strategy

### Backend Testing

- **Unit Tests**: `pytest` for individual functions and models
- **API Tests**: `pytest` for endpoint testing
- **Integration Tests**: Database interaction verification

### Frontend Testing

- **Unit Tests**: `Vitest` for component testing
- **E2E Tests**: `Playwright` with Page Object Model pattern
- **Visual Tests**: Component rendering and interaction

### CI/CD Testing

- Automated test execution on pull requests
- Build verification and deployment checks
- Cross-environment compatibility testing

## 📊 Monitoring & Quality

- **Code Coverage**: Comprehensive test coverage tracking
- **Performance**: Load testing and optimization
- **Security**: Dependency scanning and vulnerability checks
- **Code Quality**: Linting and formatting standards

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Follow the Definition of Done**
4. **Submit a pull request**

### Development Commands

```bash
# Docker commands
docker compose up -d          # Start all services
docker compose down           # Stop all services
docker compose ps             # Check service status
docker compose logs [service] # View logs
docker compose restart [service] # Restart a service

# Rebuild after code changes
docker compose up -d --build api       # Rebuild API only
docker compose up -d --build frontend  # Rebuild frontend only
docker compose up -d --build           # Rebuild all

# Run tests (when test infrastructure is set up)
nx test frontend
nx test api

# Build applications
nx build frontend
nx build api

# Lint code
nx lint frontend
nx lint api
```

### Database Access

```bash
# Connect to PostgreSQL directly
docker compose exec db psql -U postgres

# Run SQL commands
docker compose exec db psql -U postgres -c "SELECT version();"
```

## � Troubleshooting

### Container Issues

**Containers won't start:**
```bash
# Check Docker is running
docker --version

# Remove old containers and volumes
docker compose down -v

# Rebuild from scratch
docker compose build --no-cache
docker compose up -d
```

**Port conflicts:**
If you see port binding errors, check if ports are already in use:
- Frontend: 3000
- API: 8000
- Database: 54322
- PostgREST: 54321
- Inbucket: 54324, 54325, 54326

**View detailed logs:**
```bash
docker compose logs --tail=100 [service-name]
```

### Database Connection Issues

```bash
# Verify database is healthy
docker compose ps db

# Check database logs
docker compose logs db

# Test connection manually
docker compose exec db psql -U postgres -c "SELECT 1;"
```

### Frontend/Backend Communication Issues

1. Visit http://localhost:3000 to see the communication test page
2. Check that all status indicators show as healthy
3. Verify containers are on the same network:
   ```bash
   docker network inspect meal-mind-network
   ```

## �📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern web technologies
- Inspired by the need for better household management
- Designed with scalability and maintainability in mind

---

**Happy meal planning! 🍽️✨**
