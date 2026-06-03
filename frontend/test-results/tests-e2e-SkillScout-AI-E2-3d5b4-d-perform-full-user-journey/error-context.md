# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: tests/e2e.spec.ts >> SkillScout AI E2E Flow >> Should perform full user journey
- Location: tests/e2e.spec.ts:7:3

# Error details

```
TimeoutError: page.waitForURL: Timeout 10000ms exceeded.
=========================== logs ===========================
waiting for navigation to "http://localhost:5173/dashboard" until "load"
============================================================
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - generic [ref=e5]:
      - link "SkillScout AI" [ref=e6] [cursor=pointer]:
        - /url: /
        - img [ref=e8]
        - generic [ref=e11]: SkillScout AI
      - navigation [ref=e12]:
        - link "Discover" [ref=e13] [cursor=pointer]:
          - /url: /dashboard
          - img [ref=e14]
          - text: Discover
      - generic [ref=e17]:
        - link "Log in" [ref=e18] [cursor=pointer]:
          - /url: /login
          - button "Log in" [ref=e19]
        - link "Sign up" [ref=e20] [cursor=pointer]:
          - /url: /login?signup=true
          - button "Sign up" [ref=e21]
  - main [ref=e22]:
    - generic [ref=e24]:
      - generic [ref=e25]:
        - img [ref=e27]
        - heading "Create an account" [level=2] [ref=e30]
        - paragraph [ref=e31]: Sign up to start saving and tracking opportunities
      - generic [ref=e32]:
        - generic [ref=e33]:
          - text: Full Name
          - textbox "John Doe" [ref=e34]: End-to-End User
        - generic [ref=e35]:
          - text: Email
          - textbox "name@example.com" [ref=e36]: testuser_1779824696944@example.com
        - generic [ref=e37]:
          - text: Password
          - textbox "••••••••" [ref=e38]: Password123!
        - paragraph [ref=e39]: An error occurred during signup.
        - button "Sign Up" [ref=e40] [cursor=pointer]
      - generic [ref=e41]:
        - text: Already have an account?
        - button "Log in" [ref=e42] [cursor=pointer]
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
  9  |     await page.goto('http://localhost:5173/');
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
> 26 |     await page.waitForURL('http://localhost:5173/dashboard', { timeout: 10000 });
     |                ^ TimeoutError: page.waitForURL: Timeout 10000ms exceeded.
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