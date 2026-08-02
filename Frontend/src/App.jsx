import { useCallback, useEffect, useState } from "react";

import { api } from "./api.js";
import Contactos from "./componentes/Contactos.jsx";
import Pipeline from "./componentes/Pipeline.jsx";
import ReporteMensual from "./componentes/ReporteMensual.jsx";

export default function App() {
  const [deals, setDeals] = useState([]);
  // Cambiar esta version remonta Contactos, que asi vuelve a pedir su lista.
  const [version, setVersion] = useState(0);

  const recargarDeals = useCallback(async () => {
    setDeals(await api.listarDeals());
  }, []);

  useEffect(() => {
    recargarDeals();
  }, [recargarDeals]);

  async function sembrar() {
    await api.sembrar();
    await recargarDeals();
    setVersion((n) => n + 1);
  }

  return (
    <>
      <header className="cabecera">
        <h1>Micro-CRM</h1>
        <span>workshop · repo de demostracion</span>
        <button className="primario" onClick={sembrar}>
          Cargar datos de ejemplo
        </button>
      </header>

      <div className="grid">
        <ReporteMensual deals={deals} />
        <div className="grid columnas">
          <Contactos key={version} />
          <Pipeline deals={deals} alCambiar={recargarDeals} />
        </div>
      </div>
    </>
  );
}
