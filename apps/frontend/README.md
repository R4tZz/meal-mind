# MealMind Frontend 🎨

The SvelteKit-based frontend application for MealMind, a household assistant that streamlines meal planning, grocery list generation, and shopping notifications.

## Overview

This frontend provides an intuitive user interface for:

- **Recipe Management** - Browse, create, and organize recipes
- **Meal Planning** - Plan weekly meals with drag-and-drop interface
- **Grocery Lists** - View auto-generated shopping lists from planned meals
- **Smart Notifications** - Receive timely reminders for grocery shopping

## Technology Stack

- **SvelteKit** - Modern web framework with SSR support
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **shadcn/svelte** - Beautiful UI components
- **Docker** - Containerized deployment

## Development

### Prerequisites

- Node.js 20+ (for local development)
- Docker Desktop (for containerized deployment)

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open in browser
npm run dev -- --open
```

The development server runs at `http://localhost:5173` with hot module replacement.

### Building

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Docker Deployment

This application is containerized with a multi-stage Docker build optimized for production:

```bash
# Build Docker image
docker build -t meal-mind-frontend .

# Run container
docker run -p 3000:3000 meal-mind-frontend
```

The containerized app runs at `http://localhost:3000` with server-side rendering enabled.

### Docker Features

- **Multi-stage build** - Optimized production image
- **Non-root user** - Enhanced security
- **Health checks** - Container monitoring
- **Alpine Linux** - Minimal attack surface

## Integration

This frontend communicates with:

- **Backend API** - FastAPI service at `http://localhost:8000`
- **Supabase** - Authentication and real-time data
- **Docker Compose** - Orchestrated with other services

## Testing

```bash
# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e

# Type checking
npm run check
```

## Architecture

The frontend follows SvelteKit conventions with:

```
src/
├── routes/           # Page components and API routes
├── lib/             # Reusable components and utilities
├── app.html         # HTML template
└── app.css          # Global styles with Tailwind
```

Built for production deployment with `@sveltejs/adapter-node` for Node.js server environments.
