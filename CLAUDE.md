# Micro-CRM

CRM minimo para gestionar contactos, oportunidades (deals) y reportes comerciales.

## Estructura del repositorio

Dos mitades independientes. Todo comando de Python se corre **desde `Backend/`**:
ahi vive `pyproject.toml`, y pytest lo necesita para resolver sus rutas.

```
Backend/    API en Python (src/, tests/, pyproject.toml)
Frontend/   Interfaz en React + Vite
docs/       Issues del workshop y utilidades
```

## Como correr

```bash
cd Backend
pip install -e ".[dev]"
pytest                              # suite completa
uvicorn microcrm.api:app --reload
```

Para la interfaz, en otra terminal: `cd Frontend && npm run dev`.

## Arquitectura

Tres capas, con una regla estricta entre ellas:

| Capa | Archivo | Responsabilidad |
|---|---|---|
| API | `Backend/src/microcrm/api.py` | HTTP. No contiene reglas de negocio. |
| Servicios | `Backend/src/microcrm/services/` | Reglas de negocio. **Nunca escriben SQL.** |
| Repositorio | `Backend/src/microcrm/repository.py` | Todo el SQL del proyecto vive aqui. |

Si necesitas una consulta nueva, agrega una funcion en `Backend/src/microcrm/repository.py` y llamala
desde el servicio. No pongas SQL en `services/` ni en `api.py`.

## Convenciones

- El dominio se escribe en espanol (`Contacto`, `Deal`, `Etapa`, `mover_a_etapa`).
- Los errores de negocio heredan de `ErrorDeDominio`; la capa API los traduce a HTTP.
- Los servicios reciben `db: Database` como primer argumento.
- Las fechas se guardan en SQLite como texto `'YYYY-MM-DD HH:MM:SS'`.
  SQLite no tiene tipo fecha: **toda comparacion de fechas es comparacion de cadenas.**

## Tests

- `pytest`, sin mocks. Cada test usa una base SQLite en memoria (fixture `db`).
- Los helpers compartidos viven en `Backend/tests/conftest.py`.
- Nombres de test descriptivos y en espanol: `test_reporte_excluye_otros_meses`.
- Todo arreglo de bug entra con un test de regresion que falle antes del cambio.

## Al trabajar en este repo

- Antes de tocar codigo, reproduce el problema con un test que falle.
- No modifiques tests existentes para que pasen: si un test estorba, explica por que.
- Corre la suite completa antes de dar por terminado un cambio.
