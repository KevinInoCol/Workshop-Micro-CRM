# Micro-CRM

CRM minimo de contactos, oportunidades y reportes comerciales.
Repo base del workshop **Claude Code en Produccion: de Issue Tecnico a Pull Request**.

## Instalacion

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest
```

Deberias ver **16 tests en verde**.

## Levantar la API

```bash
.venv/bin/uvicorn microcrm.api:app --reload
```

Documentacion interactiva en http://localhost:8000/docs

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
