# Project: MealMind

**Project Goal:** To create a personal web application that acts as a household assistant, streamlining meal planning, automating grocery list generation, and facilitating timely communication of shopping needs.

**Technology Stack:**

- **Backend:** FastAPI (Python)
- **Frontend:** SvelteKit (JavaScript/TypeScript)
- **Database:** PostgreSQL (via Local Supabase for development, cloud Supabase for deployment)
- **Containerization:** Docker & Docker Compose
- **Monorepo Tool:** Nx
- **Python Package Manager:** `uv`
- **Styling:** Tailwind CSS
- **UI Components:** `shadcn/svelte`
- **Email Notifications:** Python `smtplib` with Gmail App Passwords
- **Testing - Backend:** `pytest` (Unit, API, Database Integration)
- **Testing - Frontend:** `Vitest` (Unit) + `Playwright` (E2E with Page Object Model)
- **CI/CD:** GitHub Actions

---

## **Project Management Methodology: Scrum & GitHub Projects**

To simulate a corporate environment with Scrum, we will use GitHub Projects as our task board.

- **Product Backlog:** All phases and their detailed requirements will serve as our initial Product Backlog. Each requirement/task will be represented as an "Issue" or "Card" in GitHub Projects.
- **Sprints:** We will define time-boxed iterations, typically **1-2 weeks long**, called Sprints. At the beginning of each Sprint (Sprint Planning), a subset of tasks from the Product Backlog will be moved into the "Sprint Backlog" (the "To Do" column on your board).
- **GitHub Project Board Setup:**
  1.  Create a new GitHub Project for your repository (or an organization if preferred).
  2.  Set up a basic Kanban board with columns like:
      - **Backlog:** All unassigned tasks from the project plan.
      - **To Do (Sprint Backlog):** Tasks committed for the current Sprint.
      - **In Progress:** Tasks currently being worked on.
      - **In Review / Testing:** Tasks ready for code review or dedicated testing.
      - **Done:** Completed tasks that meet the Definition of Done.
  3.  Each task (e.g., "Implement Recipe Model," "Create Recipe List UI") should be an issue/card.
- **Definition of Done (DoD):** For any task to be moved to "Done," it _must_ meet these criteria:
  - Code is written.
  - **Unit Tests are written and pass.**
  - **Integration/API Tests (Backend) or E2E Tests (Frontend) are written and pass** where applicable.
  - Code is reviewed (self-review for solo project, or peer review if collaborating).
  - Code is merged to `main` branch.
  - Documentation (if any) is updated.
- **Daily Stand-ups (Self-Reflection):** Each day, before coding, quickly assess:
  - What did I do yesterday?
  - What will I do today?
  - Are there any blockers?
- **Sprint Review/Retrospective:** At the end of each Sprint, evaluate what was accomplished, what went well, and what could be improved for the next Sprint.

---

## **Phase 1: Planning, Nx Monorepo & Containerized Setup**

**Overall Goal:** Establish the core Nx monorepo, containerization, database, and local development environment, including initial setup of all testing tools.

### **Requirements:**

- Define the core functional areas of the **MealMind** application.
- Select the technology stack and confirm its integration points.
- Establish the Nx monorepo structure for polyglot development.
- Implement Docker containers for frontend, backend, and a local Supabase stack.
- Configure `uv` as the Python package manager for the backend.
- Set up local development environment with all necessary tools.
- Integrate and configure chosen testing tools for both frontend and backend.

### **Acceptance Criteria (for this Phase, to move to "Done"):**

1.  **Containerized Architecture Understanding:** You can articulate (or draw a simple sketch of) how the SvelteKit frontend container will communicate with the FastAPI backend container, which in turn interacts with a **local Supabase PostgreSQL container**. All services will be orchestrated via `docker compose` within the `MealMind` Nx monorepo.
    - **Visual Representation:** `User Browser <--> SvelteKit Frontend Container (Nx Project) <--> FastAPI Backend Container (Nx Project) <--> Supabase Local Stack (PostgreSQL Container)`
2.  **Nx Workspace Initialized:**
    - An Nx monorepo workspace named `mealmind` (or `meal-mind`) is created at the root level.
    - The workspace uses your preferred package manager (npm, yarn, pnpm).
3.  **Local Supabase Stack Running via Docker:**
    - Docker Desktop (or equivalent container runtime) is installed and running.
    - The Supabase CLI is installed (`npm install supabase --save-dev` or `brew install supabase/supabase/supabase`).
    - Inside the Nx workspace root, a `supabase` directory is initialized (`npx supabase init`).
    - The local Supabase stack (including PostgreSQL, Auth, PostgREST) can be started successfully using `npx supabase start`.
    - You can access Supabase Studio locally (usually `http://localhost:54323`).
    - You have confirmed local database credentials for the Supabase Postgres instance.
4.  **Backend Application Dockerization (FastAPI + `uv`):**
    - A `Dockerfile` is created for the FastAPI application within its Nx project directory (e.g., `apps/api/Dockerfile`).
    - The `Dockerfile` uses a Python base image, installs `uv` within the container, and uses `uv` to manage dependencies (e.g., `RUN uv sync --frozen`).
    - A `pyproject.toml` and `uv.lock` file are generated for the FastAPI project to define and lock dependencies using `uv`.
    - The FastAPI application is configured to connect to the local Supabase PostgreSQL container using environment variables.
    - The backend container can be built (`docker build`) and run locally.
    - **Testing Tools Setup (Backend):** `pytest` is installed as a dev dependency for the backend project, and a minimal `pytest` configuration (e.g., `pytest.ini`) is present.
5.  **Frontend Application Dockerization (SvelteKit):**
    - A `Dockerfile` is created for the SvelteKit application within its Nx project directory (e.g., `apps/frontend/Dockerfile`).
    - The `Dockerfile` uses a Node.js base image and is set up for a multi-stage build.
    - SvelteKit is configured to use `@sveltejs/adapter-node` for server-side rendering.
    - Tailwind CSS and `shadcn/svelte` are correctly configured within the SvelteKit project.
    - The frontend container can be built (`docker build`) and run locally.
    - \*\*Testing Tools Setup (Frontend):` Vitest` and `Playwright` are installed as dev dependencies for the frontend project, and initial configurations are present.
6.  **Monorepo `docker-compose.yml` for Orchestration:**
    - A `docker-compose.yml` file is created at the root of the Nx workspace that orchestrates your local Supabase services, FastAPI backend, and SvelteKit frontend containers.
    - All containers can be brought up and shut down together using `docker compose up -d` and `docker compose down`.
    - Network configuration ensures inter-container communication via service names.
7.  **Local Development Environment Ready:**
    - Python (3.9+) and Node.js (LTS) are installed locally.
    - Nx CLI is installed globally or used via `npx`.
    - `uv` is installed globally on your host machine.
    - Your IDE (VS Code recommended) has relevant extensions.
    - `.env` files (or similar environment variable management) are correctly set up.
8.  **Initial Communication Test:**
    - You can verify that the frontend container can successfully make a simple HTTP request to the backend container.
    - The backend container can successfully connect to the local Supabase PostgreSQL database.
    - **Basic Test Confirmation:** Run a simple `nx test frontend` and `nx test api` command, confirming that the test runners execute (even if no meaningful tests are written yet beyond setup confirmation).

---

## **Phase 2: Core Backend Development & Testing**

**Overall Goal:** Establish the robust API for managing recipes, meal plans, and generating grocery lists, ensuring it's thoroughly tested as developed.

### **Requirements:**

- **Database Schema Implementation:** Implement the database schema for recipes, ingredients, and meal plans using `alembic` migrations.
- **Recipe Management API & Logic:**
  - Implement endpoints to create, retrieve (all/by ID), update, and delete recipes.
  - Implement underlying logic for handling ingredients associated with recipes.
- **Meal Planning API & Logic:**
  - Implement endpoints to add/assign recipes to specific dates and meal types.
  - Implement endpoints to retrieve, update, and remove planned meals.
- **Grocery List Generation API & Logic:**
  - Implement the core logic to aggregate ingredients from planned meals and sum quantities.
  - Create an endpoint to expose the consolidated grocery list.
- **CORS Configuration:** Properly configure CORS in FastAPI.

### **Acceptance Criteria (for each task within this phase):**

- **Code is Written:** All required API endpoints and business logic are implemented.
- **Backend Unit Tests:** Unit tests for individual functions, models, and utility modules are written and pass.
- **Backend API/Integration Tests:** API tests covering all implemented endpoints are written using `pytest`. These tests verify:
  - Correct status codes (200 OK, 201 Created, 400 Bad Request, 404 Not Found, etc.).
  - Accurate request/response body structures (using Pydantic models).
  - Correct data persistence and retrieval from the PostgreSQL database (using test fixtures that manage transaction rollbacks or a dedicated test database).
  - Error handling scenarios (e.g., invalid input, non-existent IDs).
- **Database Interaction Verified:** Specific tests confirm that `alembic` migrations apply correctly and that SQLAlchemy ORM interactions perform as expected with the database.
- **CORS Functionality:** Basic test or manual verification that CORS headers are correctly returned.
- All tests for the implemented feature pass consistently.
- Code is reviewed and merged to `main`.

---

## **Phase 3: Frontend Development & Testing**

**Overall Goal:** Build the interactive user interface for managing recipes, planning meals, and viewing grocery lists, ensuring robust frontend testing during development.

### **Requirements:**

- **Frontend Architecture:** Structure the SvelteKit application using layouts, pages, and components.
- **Recipe Management UI:**
  - Develop components and pages to display a list of all recipes.
  - Implement forms for adding new recipes, including dynamic fields for ingredient input.
  - Create UI for editing and deleting existing recipes.
- **Meal Planning UI:**
  - Develop a component to visualize the weekly meal plan (e.g., a simple grid or calendar view).
  - Implement functionality to select recipes and assign them to specific days/meal slots.
  - Add UI to remove planned meals.
- **Grocery List UI:**
  - Develop a page/component to display the generated grocery list clearly.
  - Implement interactive checkboxes/toggles for items (local state for now).
- **API Integration:** All UI components effectively communicate with the FastAPI backend.
- **Styling:** Apply consistent styling using Tailwind CSS and `shadcn/svelte` components.

### **Acceptance Criteria (for each task within this phase):**

- **Code is Written:** All required UI components and pages are implemented.
- **Frontend Unit Tests:** Unit tests for individual Svelte components, utility functions, and stores are written using `Vitest` and pass. These tests verify:
  - Component rendering based on props.
  - Internal component logic and state updates.
  - Event handling.
- **End-to-End (E2E) Tests with Playwright & POM:** E2E tests for critical user workflows are written using `Playwright` and the Page Object Model (POM) pattern. These tests verify:
  - Successful navigation between pages.
  - Correct display and interaction with UI elements.
  - Accurate data fetching and display from the backend.
  - Successful submission of forms and data changes to the backend.
  - Key user journeys (e.g., adding a recipe -> planning it -> viewing it on grocery list).
- All tests for the implemented feature pass consistently.
- Code is reviewed and merged to `main`.

---

## **Phase 4: Notifications & Scheduling with Testing**

**Overall Goal:** Implement the automated email notification system for grocery lists, ensuring comprehensive testing.

### **Requirements:**

- **Email Sending Logic:** Implement a utility function for sending formatted HTML emails using Python's `smtplib`.
- **Backend Notification Endpoint:** Create a FastAPI endpoint (e.g., `POST /send_grocery_list_email`) that triggers the email sending function for the current week's list.
- **Frontend Trigger:** Add a button/action in the frontend UI to manually trigger the "Send Grocery List Email" via the backend endpoint.
- **Automated Scheduling:** Implement a mechanism to call the notification endpoint automatically at a predefined time (e.g., using a separate Python process with `schedule` library run by a `cron` job/Task Scheduler on the host/dedicated container).

### **Acceptance Criteria (for each task within this phase):**

- **Code is Written:** All required notification logic and endpoints are implemented.
- **Backend Unit Tests:** Unit tests for the email formatting utility and any complex scheduling logic are written and pass.
- **Backend API Tests:** API tests for the `/send_grocery_list_email` endpoint are written and pass. These tests verify:
  - Correct request handling and response.
  - The email sending utility is correctly invoked (mocking the actual SMTP send call to avoid sending real emails during tests).
- **Frontend E2E Test (if applicable):** An E2E test confirms that the "Send Email" button/action in the UI successfully triggers the backend endpoint.
- **Scheduling Verified (Manual/Observational):** Automated scheduling mechanism is set up and observed to trigger the email sending at the specified time (manual verification in development, or a simple log check).
- All tests for the implemented feature pass consistently.
- Code is reviewed and merged to `main`.

---

## **Phase 5: Deployment & CI/CD**

**Overall Goal:** Deploy the MealMind application to a public cloud environment and establish automated testing in the CI/CD pipeline.

### **Requirements:**

- **Backend Deployment:** Deploy the FastAPI application container to a free-tier cloud platform.
- **Frontend Deployment:** Deploy the SvelteKit application container to a suitable hosting provider.
- **Database Configuration:** Configure the deployed FastAPI backend to connect to a live (non-local) Supabase project.
- **CI/CD Pipeline Setup (GitHub Actions):**
  - Create GitHub Actions workflows to automate:
    - Building both frontend and backend applications within the Nx monorepo.
    - **Running all unit, API, and E2E tests** on code pushes to the `main` branch or pull requests.
    - (Optional but recommended) Deploying to staging/production environments upon successful tests/manual approval.
- **Environment Variable Management:** Securely manage environment variables for deployment.

### **Acceptance Criteria:**

- The deployed application is publicly accessible via URLs for both frontend and backend.
- All features work correctly in the deployed environment, connecting to the cloud Supabase instance.
- GitHub Actions workflows are correctly configured and trigger automatically.
- **All tests (unit, API, E2E) run successfully within the GitHub Actions CI/CD pipeline.**
- The CI/CD pipeline clearly indicates build and test status.
- Deployment artifacts (Docker images, static files) are successfully built and pushed.

---

## **Phase 6: Refinement & Iteration**

**Overall Goal:** Continuously improve the MealMind application based on user feedback and explore advanced features.

### **Requirements:**

- Gather and prioritize user feedback (from your wife!).
- Implement selected improvements, bug fixes, or new minor features.
- Explore advanced features like user authentication, multi-user support, recipe importing, or pantry tracking.

### **Acceptance Criteria:**

- User feedback is systematically collected and reviewed.
- Prioritized improvements are implemented and tested, moving through the standard development workflow (Scrum).
- The application continues to function stably and reliably after iterations.

---
