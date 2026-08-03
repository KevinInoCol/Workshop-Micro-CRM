# Micro-CRM

CRM minimo de contactos, oportunidades y reportes comerciales.
Repo base del workshop **Claude Code en Produccion: de Issue Tecnico a Pull Request**.

El proyecto son dos piezas independientes:

```
Backend/    API en Python (FastAPI + SQLite)
Frontend/   Interfaz en React + Vite
```

## Backend

Todos los comandos de Python se corren **desde `Backend/`**, que es donde vive
`pyproject.toml`.

Con **conda**:

```bash
cd Backend
conda create -n Workshop-26-Micro-CRM python=3.12 -y
conda activate Workshop-26-Micro-CRM
pip install -e ".[dev]"
```

O con **venv**:

```bash
cd Backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

Con el entorno activo:

```bash
pytest                              # deberias ver 16 tests en verde
uvicorn microcrm.api:app --reload
```

API en http://localhost:8000 · documentacion interactiva en `/docs`

## Frontend

En otra terminal, desde la raiz del repositorio:

```bash
cd Frontend
npm install
npm run dev
```

Interfaz en http://localhost:5173

Vite hace de proxy hacia el backend, asi que el navegador ve un solo origen y no
hay CORS de por medio. Si tu backend no esta en el puerto 8000:

```bash
VITE_BACKEND=http://localhost:8010 npm run dev
```

Tambien puedes compilar la interfaz (`npm run build`) y dejar que la sirva el
propio backend desde `/`.

## Endpoints

| Metodo | Ruta | Descripcion |
|---|---|---|
| `POST` | `/contactos` | Crea un contacto |
| `GET` | `/contactos?q=` | Busca por nombre o empresa |
| `POST` | `/deals` | Crea una oportunidad |
| `PATCH` | `/deals/{id}/etapa` | Mueve un deal de etapa |
| `GET` | `/pipeline` | Monto abierto por etapa |
| `GET` | `/reportes/mensual?anio=&mes=` | Cierres del mes |
| `GET` | `/reportes/comparativa?anio=&mes=` | Mes actual vs mes anterior |

## Modelo de dominio

Un **Contacto** tiene N **Deals**. Cada deal recorre el pipeline:

```
nuevo → contactado → propuesta → negociacion → ganado
                                             ↘ perdido
```

`ganado` y `perdido` son etapas terminales: al entrar en ellas se sella `cerrado_en`.

## Para el workshop

- `CLAUDE.md` — convenciones que Claude Code lee automaticamente.
- `docs/` — issues preparados, rubrica de revision y guia del instructor.
