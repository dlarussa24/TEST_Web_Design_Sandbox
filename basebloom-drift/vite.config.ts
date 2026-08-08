import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/basebloom/',
  build: {
    outDir: '../public/basebloom',
    // MUST stay false. The output dir also holds hand-placed runtime assets
    // that Vite does not generate — the self-hosted hero loop (mp4 + webm)
    // and fonts/. Emptying it on build deletes them.
    emptyOutDir: false,
  },
});
