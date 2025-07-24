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
- **pytest** + **httpx** - Comprehensive testing

### Frontend

- **SvelteKit** (TypeScript) - Modern web framework
- **Tailwind CSS** - Utility-first styling
- **shadcn/svelte** - Beautiful UI components
- **Vitest** + **Playwright** - Unit and E2E testing

### Infrastructure

- **Docker** + **Docker Compose** - Containerization
- **Nx** - Monorepo management
- **GitHub Actions** - CI/CD pipeline
- **Supabase** - Database and authentication

## 🏗️ Architecture

```
User Browser ↔ SvelteKit Frontend Container ↔ FastAPI Backend Container ↔ Supabase PostgreSQL
```

The application runs as a containerized microservices architecture with:

- Frontend and backend as separate Docker containers
- Local Supabase stack for development
- All services orchestrated via Docker Compose within an Nx monorepo

## 🚀 Getting Started

### Prerequisites

- **Docker Desktop** - Container runtime
- **Node.js** (LTS) - JavaScript runtime
- **Python** (3.9+) - Backend runtime
- **uv** - Python package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/R4tZz/meal-mind.git
   cd meal-mind
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Initialize Supabase**

   ```bash
   npx supabase init
   npx supabase start
   ```

4. **Start the development environment**

   ```bash
   docker compose up -d
   ```

5. **Access the application**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - Supabase Studio: `http://localhost:54323`

## 📋 Development Workflow

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
- [x] Docker containerization
- [x] Local Supabase stack
- [ ] Testing infrastructure

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
- **API Tests**: `httpx` for endpoint testing
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
# Run tests
nx test frontend
nx test api

# Build applications
nx build frontend
nx build api

# Lint code
nx lint frontend
nx lint api

# Start development servers
nx serve frontend
nx serve api
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern web technologies
- Inspired by the need for better household management
- Designed with scalability and maintainability in mind

---

**Happy meal planning! 🍽️✨**
