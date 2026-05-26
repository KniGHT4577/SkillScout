# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: tests/e2e.spec.ts >> SkillScout AI E2E Flow >> Should perform full user journey
- Location: tests/e2e.spec.ts:7:3

# Error details

```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:5173/
Call log:
  - navigating to "http://localhost:5173/", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  |
  3  | test.describe('SkillScout AI E2E Flow', () => {
  4  |   const testEmail = `testuser_${Date.now()}@example.com`;
  5  |   const testPassword = 'Password123!';
  6  |
  7  |   test('Should perform full user journey', async ({ page }) => {
  8  |     // 1. Landing Page
> 9  |     await page.goto('http://localhost:5173/');
     |                ^ Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:5173/
  10 |     await expect(page.locator('h1')).toContainText('Supercharge your career');
  11 |
  12 |     // 2. Auth Flow (Wait for hydration if necessary)
  13 |     await page.waitForSelector('text="Sign In"');
  14 |     await page.click('text="Sign In"');
  15 |     await page.waitForURL('http://localhost:5173/login');
  16 |
  17 |     // Switch to Sign Up
  18 |     await page.click('text="Sign up"');
  19 |
  20 |     await page.fill('input[type="text"]', 'End-to-End User');
  21 |     await page.fill('input[type="email"]', testEmail);
  22 |     await page.fill('input[type="password"]', testPassword);
  23 |     await page.click('button[type="submit"]');
  24 |
  25 |     // Should navigate to dashboard eventually
  26 |     await page.waitForURL('http://localhost:5173/dashboard', { timeout: 10000 });
  27 |
  28 |     // 3. Dashboard Functionality
  29 |     await expect(page.locator('h1')).toContainText('Discover');
  30 |
  31 |     // Wait for the mock seed data to load (cards should exist)
  32 |     await page.waitForSelector('.group', { timeout: 10000 }); // Cards have .group class
  33 |
  34 |     // Search
  35 |     await page.fill('input[placeholder="Search opportunities..."]', 'Harvard');
  36 |     await page.waitForTimeout(1000); // Wait for debounce
  37 |
  38 |     // 4. Bookmark
  39 |     // Look for the first bookmark button inside a card
  40 |     const firstCard = page.locator('.group').first();
  41 |     const bookmarkBtn = firstCard.locator('button');
  42 |     await bookmarkBtn.click();
  43 |     await page.waitForTimeout(1000); // Wait for animation
  44 |
  45 |     // 5. Bookmarks Page
  46 |     await page.click('text="Bookmarks"');
  47 |     await page.waitForURL('http://localhost:5173/bookmarks');
  48 |     await expect(page.locator('h1')).toContainText('Your Bookmarks');
  49 |
  50 |     // The bookmarked card should appear here
  51 |     await expect(page.locator('.group')).toHaveCount(1);
  52 |   });
  53 | });
  54 |
```