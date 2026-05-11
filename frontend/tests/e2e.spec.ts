import { test, expect } from '@playwright/test';

test.describe('SkillScout AI E2E Flow', () => {
  const testEmail = `testuser_${Date.now()}@example.com`;
  const testPassword = 'Password123!';

  test('Should perform full user journey', async ({ page }) => {
    // 1. Landing Page
    await page.goto('http://localhost:5173/');
    await expect(page.locator('h1')).toContainText('Supercharge your career');
    
    // 2. Auth Flow (Wait for hydration if necessary)
    await page.waitForSelector('text="Sign In"');
    await page.click('text="Sign In"');
    await page.waitForURL('http://localhost:5173/login');
    
    // Switch to Sign Up
    await page.click('text="Sign up"');
    
    await page.fill('input[type="text"]', 'End-to-End User');
    await page.fill('input[type="email"]', testEmail);
    await page.fill('input[type="password"]', testPassword);
    await page.click('button[type="submit"]');

    // Should navigate to dashboard eventually
    await page.waitForURL('http://localhost:5173/dashboard', { timeout: 10000 });
    
    // 3. Dashboard Functionality
    await expect(page.locator('h1')).toContainText('Discover');

    // Wait for the mock seed data to load (cards should exist)
    await page.waitForSelector('.group', { timeout: 10000 }); // Cards have .group class
    
    // Search
    await page.fill('input[placeholder="Search opportunities..."]', 'Harvard');
    await page.waitForTimeout(1000); // Wait for debounce

    // 4. Bookmark
    // Look for the first bookmark button inside a card
    const firstCard = page.locator('.group').first();
    const bookmarkBtn = firstCard.locator('button');
    await bookmarkBtn.click();
    await page.waitForTimeout(1000); // Wait for animation
    
    // 5. Bookmarks Page
    await page.click('text="Bookmarks"');
    await page.waitForURL('http://localhost:5173/bookmarks');
    await expect(page.locator('h1')).toContainText('Your Bookmarks');
    
    // The bookmarked card should appear here
    await expect(page.locator('.group')).toHaveCount(1);
  });
});
