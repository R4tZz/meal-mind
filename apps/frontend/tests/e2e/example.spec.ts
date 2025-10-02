import { test, expect } from '@playwright/test';

test('homepage has title', async ({ page }) => {
	await page.goto('/');
	
	// Expect the page to have a title
	await expect(page).toHaveTitle(/MealMind/);
});
