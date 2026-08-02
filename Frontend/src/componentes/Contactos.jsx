import { useEffect, useState } from "react";

import { api } from "../api.js";

const VACIO = { nombre: "", email: "", empresa: "" };

export default function Contactos() {
  const [contactos, setContactos] = useState([]);
  const [formulario, setFormulario] = useState(VACIO);
  const [busqueda, setBusqueda] = useState("");
  const [aviso, setAviso] = useState("");

  async function cargar(termino = busqueda) {
    setContactos(await api.buscarContactos(termino));
  }

  useEffect(() => {
    cargar("");
  }, []);

  async function agregar(evento) {
    evento.preventDefault();
    setAviso("");
    try {
      await api.crearContacto({
        nombre: formulario.nombre,
        email: formulario.email,
        empresa: formulario.empresa || null,
      });
      setFormulario(VACIO);
      cargar();
    } catch (error) {
      setAviso(error.message);
    }
  }

  const campo = (clave, marcador, requerido = false) => (
    <input
      placeholder={marcador}
      required={requerido}
      value={formulario[clave]}
      onChange={(e) => setFormulario({ ...formulario, [clave]: e.target.value })}
    />
  );

  return (
    <section className="tarjeta">
      <h2>Contactos</h2>

      <form onSubmit={agregar}>
        {campo("nombre", "Nombre", true)}
        {campo("email", "Email", true)}
        {campo("empresa", "Empresa")}
        <button className="primario">Agregar</button>
      </form>

      <form
        onSubmit={(evento) => {
          evento.preventDefault();
          cargar();
        }}
      >
        <input
          placeholder="Buscar por nombre o empresa"
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
        <button>Buscar</button>
      </form>

      <table>
        <tbody>
          {contactos.length === 0 && (
            <tr>
              <td className="tenue">Sin contactos</td>
            </tr>
          )}
          {contactos.map((contacto) => (
            <tr key={contacto.id}>
              <td>
                <strong>{contacto.nombre}</strong>
              </td>
              <td>{contacto.email}</td>
              <td className="tenue">{contacto.empresa ?? ""}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="aviso">{aviso}</div>
    </section>
  );
}
