import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
base: '/apocVanguard',
  plugins: [react()],
  envPrefix: ['VITE_'],
})
