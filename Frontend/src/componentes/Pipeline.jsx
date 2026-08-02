import { ETAPAS, api, soles } from "../api.js";

const fecha = (iso) => (iso ? iso.replace("T", " ").slice(0, 16) : "—");

export default function Pipeline({ deals, alCambiar }) {
  async function mover(id, etapa) {
    await api.moverEtapa(id, etapa);
    alCambiar();
  }

  return (
    <section className="tarjeta">
      <h2>Pipeline</h2>
      <table>
        <thead>
          <tr>
            <th>Oportunidad</th>
            <th>Etapa</th>
            <th className="num">Monto</th>
            <th>Cerrado</th>
          </tr>
        </thead>
        <tbody>
          {deals.map((deal) => (
            <tr key={deal.id}>
              <td>
                {deal.titulo}
                <br />
                <span className="tenue">{deal.contacto}</span>
              </td>
              <td>
                <select
                  value={deal.etapa}
                  onChange={(evento) => mover(deal.id, evento.target.value)}
                >
                  {ETAPAS.map((etapa) => (
                    <option key={etapa} value={etapa}>
                      {etapa}
                    </option>
                  ))}
                </select>
              </td>
              <td className="num">{soles(deal.monto)}</td>
              <td className="tenue">{fecha(deal.cerrado_en)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
