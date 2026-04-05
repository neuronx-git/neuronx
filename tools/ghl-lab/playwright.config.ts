import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  timeout: 5 * 60 * 1000,
  use: {
    headless: false,
  },
})

