/** Cliente HTTP del Micro-CRM. Vite hace de proxy hacia el backend. */

async function pedir(url, opciones) {
  const respuesta = await fetch(url, opciones);
  const cuerpo = await respuesta.json().catch(() => null);
  if (!respuesta.ok) {
    throw new Error(cuerpo?.detail ?? respuesta.statusText);
  }
  return cuerpo;
}

const conCuerpo = (metodo, datos) => ({
  method: metodo,
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(datos),
});

export const api = {
  buscarContactos: (q = "") => pedir(`/contactos?q=${encodeURIComponent(q)}`),
  crearContacto: (contacto) => pedir("/contactos", conCuerpo("POST", contacto)),

  listarDeals: () => pedir("/deals"),
  moverEtapa: (id, etapa) => pedir(`/deals/${id}/etapa`, conCuerpo("PATCH", { etapa })),

  reporteMensual: (anio, mes) => pedir(`/reportes/mensual?anio=${anio}&mes=${mes}`),

  sembrar: () => pedir("/demo/sembrar", { method: "POST" }),
};

export const soles = (n) => `S/ ${(n ?? 0).toLocaleString("es-PE")}`;

export const ETAPAS = [
  "nuevo",
  "contactado",
  "propuesta",
  "negociacion",
  "ganado",
  "perdido",
];

export const MESES = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
];
