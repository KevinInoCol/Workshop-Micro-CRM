import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// El backend corre aparte (uvicorn). Vite le pasa las llamadas de API
// para que el navegador vea un solo origen y no haya CORS de por medio.
const backend = process.env.VITE_BACKEND ?? "http://localhost:8000";

const rutasDeApi = ["/contactos", "/deals", "/reportes", "/pipeline", "/demo"];

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: Object.fromEntries(rutasDeApi.map((ruta) => [ruta, backend])),
  },
});
