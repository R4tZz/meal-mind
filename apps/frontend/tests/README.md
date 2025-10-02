# Testing Setup

This project uses **Vitest** for unit testing and **Playwright** for end-to-end (E2E) testing.

## Vitest (Unit Testing)

Vitest is configured in `vite.config.ts` and runs tests for components and utilities.

### Running Unit Tests

```bash
# Run tests in watch mode
npm run test

# Run tests once
npm run test -- --run

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

### Writing Unit Tests

Create test files with `.test.ts` or `.spec.ts` extension in the `src` directory:

```typescript
import { describe, it, expect } from 'vitest';

describe('MyComponent', () => {
  it('should work', () => {
    expect(true).toBe(true);
  });
});
```

## Playwright (E2E Testing)

Playwright is configured in `playwright.config.ts` for end-to-end testing across multiple browsers.

### Installing Browsers

Before running E2E tests for the first time, install the browsers:

```bash
npx playwright install
```

### Running E2E Tests

```bash
# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui

# Run E2E tests in debug mode
npm run test:e2e:debug
```

### Writing E2E Tests

Create test files in the `tests/e2e` directory:

```typescript
import { test, expect } from '@playwright/test';

test('homepage loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/MealMind/);
});
```

## Test Configuration Files

- **vite.config.ts** - Contains Vitest configuration
- **playwright.config.ts** - Contains Playwright configuration
- **src/test/setup.ts** - Vitest setup file for global test utilities

## CI/CD Integration

Both test suites are configured to run in CI environments. The Playwright configuration automatically handles browser installation and server startup for E2E tests.
