import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// FIX for Cloudflare: force Vite to use esbuild instead of Rolldown
export default defineConfig({
  plugins: [react()],
  build: {
    target: "esnext",
    // Cloudflare does not support rolldown native bindings
    // so we disable it explicitly
    rollupOptions: {},
  },
  optimizeDeps: {
    // Force esbuild instead of rolldown
    disabled: false,
  }
});
