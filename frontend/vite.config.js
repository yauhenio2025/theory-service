import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Build timestamp to force new bundle hash
const BUILD_TIMESTAMP = Date.now()

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    __BUILD_TIMESTAMP__: BUILD_TIMESTAMP
  },
  build: {
    // Force new hash on each build
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name]-${BUILD_TIMESTAMP}-[hash].js`,
        chunkFileNames: `assets/[name]-${BUILD_TIMESTAMP}-[hash].js`,
        assetFileNames: `assets/[name]-${BUILD_TIMESTAMP}-[hash].[ext]`
      }
    }
  }
})
