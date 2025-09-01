import { test, expect } from '@playwright/test';

test.describe('Dashboard Visual Regression Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Mock API responses
    await page.route('**/api/v1/pricing/tokens', async route => {
      await route.fulfill({
        json: [
          {
            id: '1',
            name: 'Infrastructure Scan',
            description: 'Comprehensive infrastructure analysis',
            unit_type: 'per_resource',
            base_price: 5.00,
            category: 'scanning',
            is_active: true
          }
        ]
      });
    });

    await page.route('**/api/v1/dashboard/metrics', async route => {
      await route.fulfill({
        json: {
          total_cost: 15420.50,
          security_score: 87,
          active_projects: 12,
          system_health: 'healthy'
        }
      });
    });
  });

  test('dashboard loads with correct layout', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Wait for content to load
    await page.waitForSelector('[data-testid="dashboard-content"]');
    
    // Take full page screenshot
    await expect(page).toHaveScreenshot('dashboard-full-page.png', {
      fullPage: true,
      animations: 'disabled'
    });
  });

  test('pricing calculator visual consistency', async ({ page }) => {
    await page.goto('/pricing');
    
    // Wait for service tokens to load
    await page.waitForSelector('text=Infrastructure Scan');
    
    // Take screenshot of pricing calculator
    await expect(page.locator('[data-testid="pricing-calculator"]')).toHaveScreenshot('pricing-calculator.png');
  });

  test('command palette visual appearance', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Open command palette
    await page.keyboard.press('Meta+k');
    await page.waitForSelector('[placeholder="Search commands..."]');
    
    // Take screenshot of command palette
    await expect(page.locator('[role="dialog"]')).toHaveScreenshot('command-palette.png');
  });

  test('interactive charts render correctly', async ({ page }) => {
    await page.goto('/cost-analysis');
    
    // Wait for charts to load
    await page.waitForSelector('[data-testid="bar-chart"]');
    
    // Take screenshot of charts section
    await expect(page.locator('[data-testid="charts-container"]')).toHaveScreenshot('interactive-charts.png');
  });

  test('mobile responsive layout', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/dashboard');
    
    // Wait for mobile layout
    await page.waitForSelector('[data-testid="mobile-menu"]');
    
    // Take mobile screenshot
    await expect(page).toHaveScreenshot('dashboard-mobile.png', {
      fullPage: true
    });
  });

  test('tablet responsive layout', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/dashboard');
    
    // Wait for content to load
    await page.waitForSelector('[data-testid="dashboard-content"]');
    
    // Take tablet screenshot
    await expect(page).toHaveScreenshot('dashboard-tablet.png', {
      fullPage: true
    });
  });

  test('dark theme consistency', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Verify dark theme is applied
    const bodyClass = await page.getAttribute('body', 'class');
    expect(bodyClass).toContain('bg-cyber-black');
    
    // Take screenshot to verify dark theme
    await expect(page).toHaveScreenshot('dark-theme.png', {
      fullPage: true
    });
  });

  test('loading states visual appearance', async ({ page }) => {
    // Delay API responses to capture loading states
    await page.route('**/api/v1/pricing/tokens', async route => {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await route.fulfill({
        json: []
      });
    });

    await page.goto('/pricing');
    
    // Capture loading skeleton
    await expect(page.locator('[data-testid="loading-skeleton"]')).toHaveScreenshot('loading-skeleton.png');
  });

  test('error states visual appearance', async ({ page }) => {
    // Mock API error
    await page.route('**/api/v1/pricing/tokens', async route => {
      await route.fulfill({
        status: 500,
        json: { error: 'Internal server error' }
      });
    });

    await page.goto('/pricing');
    
    // Wait for error message
    await page.waitForSelector('text=Error loading service tokens');
    
    // Take screenshot of error state
    await expect(page.locator('[data-testid="error-container"]')).toHaveScreenshot('error-state.png');
  });

  test('hover states and animations', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Hover over a card to trigger hover state
    await page.hover('[data-testid="dashboard-card"]');
    
    // Wait for animation to complete
    await page.waitForTimeout(500);
    
    // Take screenshot of hover state
    await expect(page.locator('[data-testid="dashboard-card"]')).toHaveScreenshot('card-hover-state.png');
  });

  test('form validation visual feedback', async ({ page }) => {
    await page.goto('/pricing');
    
    // Wait for form to load
    await page.waitForSelector('[data-testid="quantity-input"]');
    
    // Enter invalid data
    await page.fill('[data-testid="quantity-input"]', '-5');
    await page.click('[data-testid="calculate-button"]');
    
    // Wait for validation message
    await page.waitForSelector('[data-testid="validation-error"]');
    
    // Take screenshot of validation state
    await expect(page.locator('[data-testid="pricing-form"]')).toHaveScreenshot('form-validation.png');
  });
});
