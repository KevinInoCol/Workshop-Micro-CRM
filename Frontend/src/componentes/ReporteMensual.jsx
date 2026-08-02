import { useEffect, useState } from "react";

import { MESES, api, soles } from "../api.js";

/** Cuenta los deals ganados de un mes mirando el pipeline, sin pasar por el reporte. */
function ganadosDelMes(deals, anio, mes) {
  return deals.filter((deal) => {
    if (deal.etapa !== "ganado" || !deal.cerrado_en) return false;
    const fecha = new Date(deal.cerrado_en);
    return fecha.getFullYear() === anio && fecha.getMonth() + 1 === mes;
  });
}

export default function ReporteMensual({ deals }) {
  const [anio, setAnio] = useState(2026);
  const [mes, setMes] = useState(3);
  const [reporte, setReporte] = useState(null);

  async function cargar() {
    setReporte(await api.reporteMensual(anio, mes));
  }

  useEffect(() => {
    cargar();
    // Se recalcula cuando cambian los deals para que el control quede al dia.
  }, [deals]); // eslint-disable-line react-hooks/exhaustive-deps

  const enPipeline = ganadosDelMes(deals, anio, mes);
  const montoPipeline = enPipeline.reduce((total, deal) => total + deal.monto, 0);
  const cuadra =
    reporte &&
    enPipeline.length === reporte.deals_ganados &&
    montoPipeline === reporte.monto_ganado;

  return (
    <section className="tarjeta">
      <h2>Reporte mensual</h2>

      <form
        onSubmit={(evento) => {
          evento.preventDefault();
          cargar();
        }}
      >
        <select value={mes} onChange={(e) => setMes(Number(e.target.value))}>
          {MESES.map((nombre, indice) => (
            <option key={nombre} value={indice + 1}>
              {nombre}
            </option>
          ))}
        </select>
        <input
          type="number"
          value={anio}
          onChange={(e) => setAnio(Number(e.target.value))}
          style={{ flex: "0 0 90px" }}
        />
        <button>Ver</button>
      </form>

      {reporte && (
        <>
          <div className="cifras">
            <div className="cifra">
              <strong style={{ color: "var(--ok)" }}>{reporte.deals_ganados}</strong>
              <span>Ganados</span>
            </div>
            <div className="cifra">
              <strong style={{ color: "var(--mal)" }}>{reporte.deals_perdidos}</strong>
              <span>Perdidos</span>
            </div>
            <div className="cifra">
              <strong>{soles(reporte.monto_ganado)}</strong>
              <span>Monto ganado</span>
            </div>
            <div className="cifra">
              <strong>{Math.round(reporte.tasa_conversion * 100)}%</strong>
              <span>Conversion</span>
            </div>
          </div>

          <div className={cuadra ? "control" : "control alerta"}>
            Control: el pipeline tiene <b>{enPipeline.length}</b> deals ganados este mes por{" "}
            <b>{soles(montoPipeline)}</b>
            {cuadra ? (
              ". Cuadra con el reporte."
            ) : (
              <>
                , pero el reporte muestra <b>{reporte.deals_ganados}</b> por{" "}
                <b>{soles(reporte.monto_ganado)}</b>.
              </>
            )}
          </div>
        </>
      )}
    </section>
  );
}
