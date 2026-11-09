import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: '.', testMatch: 'dialog.spec.ts', workers: 1,
  use: { channel: 'chrome', baseURL: 'http://127.0.0.1:4183', trace: 'retain-on-failure' },
  projects: [
    { name: 'desktop-chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'narrow-chromium', use: { viewport: { width: 375, height: 667 } } },
  ],
  webServer: { command: 'npm run preview', url: 'http://127.0.0.1:4183', reuseExistingServer: false },
});
