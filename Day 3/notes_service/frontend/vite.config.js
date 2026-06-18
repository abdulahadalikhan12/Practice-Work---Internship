import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Only affects `npm run dev` (local development), NOT the production
    // build. Forwards any request the dev server gets for /notes/* over
    // to FastAPI, so App.jsx can call fetch("/notes") and have it work
    // immediately, without nginx in the picture yet. In production,
    // nginx itself does this same forwarding job (see nginx.conf).
    proxy: {
      '/notes': 'http://127.0.0.1:8000',
    },
  },
})
