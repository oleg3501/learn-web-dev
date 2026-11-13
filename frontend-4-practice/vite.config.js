import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { setupServerMiddleware } from './server/server.js'

export default defineConfig({
  plugins: [
    react(),
    {
      name: 'mock-server',
      configureServer(server) {
        setupServerMiddleware(server);
      }
    }
  ]
})