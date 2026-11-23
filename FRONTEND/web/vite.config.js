import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    // Monorepo (web + mobile): garante que bibliotecas instaladas na raiz do
    // workspace (ex.: react-chartjs-2) usem a MESMA cópia de react do app,
    // evitando o erro "resolveDispatcher() is null" (react duplicado).
    dedupe: ["react", "react-dom"],
  },
})
