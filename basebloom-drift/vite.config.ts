import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/basebloom/',
  build: {
    // Was '../public/basebloom'. That directory is now a byte-for-byte mirror
    // of the live basebloomdesign.com build, which is NOT produced by this
    // Vite app — so building here would silently overwrite the mirror's
    // index.html and assets with this older concept. Output is local now;
    // nothing in this app is deployed until that is deliberately rewired.
    outDir: 'dist',
    emptyOutDir: true,
  },
});
