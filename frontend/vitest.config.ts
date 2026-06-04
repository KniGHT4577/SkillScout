import { defineConfig } from 'vitest/config'
import path from 'path'

export default defineConfig({
  test: {
    include: ['src/**/*.test.{ts,tsx}'],
    exclude: ['tests/e2e.spec.ts', 'node_modules'],
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
