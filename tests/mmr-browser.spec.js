// Playwright smoke tests for Merkle Mountains v0.3 HTML
// Requires: npx playwright test tests/mmr-browser.spec.js
const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('Merkle Mountains browser smoke', () => {
  test.beforeEach(async ({ page }) => {
    const file = path.resolve(__dirname, '../docs/classes-with-glasses/merkle-mountains/index.html');
    await page.goto('file://' + file);
  });

  test('page loads and shows title', async ({ page }) => {
    await expect(page).toHaveTitle(/Merkle Mountains/);
    await expect(page.locator('h1')).toContainText('Merkle Mountains');
  });

  test('append sample receipts and observe peaks', async ({ page }) => {
    await page.click('#samples');
    await page.waitForTimeout(1500);
    const shape = await page.locator('#shape').textContent();
    expect(shape).toMatch(/11 leaves/);
    expect(shape).toMatch(/heights 3, 1, 0/);
  });

  test('generate inclusion proof and verify', async ({ page }) => {
    await page.click('#samples');
    await page.waitForTimeout(1500);
    await page.selectOption('#index', '0');
    await page.click('#makeproof');
    await page.waitForTimeout(500);
    await page.click('#pin');
    await page.click('#verify');
    await page.waitForTimeout(500);
    const status = await page.locator('#proofstatus').textContent();
    expect(status).toMatch(/PASS/);
  });

  test('altered claim is rejected', async ({ page }) => {
    await page.click('#samples');
    await page.waitForTimeout(1500);
    await page.selectOption('#index', '0');
    await page.click('#makeproof');
    await page.waitForTimeout(500);
    await page.click('#pin');
    await page.fill('#challenge', 'TAMPERED CLAIM');
    await page.click('#verify');
    await page.waitForTimeout(500);
    const status = await page.locator('#proofstatus').textContent();
    expect(status).toMatch(/FAIL|changed/);
  });
});
