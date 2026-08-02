# Micro-CRM

CRM minimo para gestionar contactos, oportunidades (deals) y reportes comerciales.

## Como correr

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest          # suite completa
.venv/bin/uvicorn microcrm.api:app --reload
```

## Arquitectura

Tres capas, con una regla estricta entre ellas:

| Capa | Archivo | Responsabilidad |
|---|---|---|
| API | `src/microcrm/api.py` | HTTP. No contiene reglas de negocio. |
| Servicios | `src/microcrm/services/` | Reglas de negocio. **Nunca escriben SQL.** |
| Repositorio | `src/microcrm/repository.py` | Todo el SQL del proyecto vive aqui. |

Si necesitas una consulta nueva, agrega una funcion en `repository.py` y llamala
desde el servicio. No pongas SQL en `services/` ni en `api.py`.

## Convenciones

- El dominio se escribe en espanol (`Contacto`, `Deal`, `Etapa`, `mover_a_etapa`).
- Los errores de negocio heredan de `ErrorDeDominio`; la capa API los traduce a HTTP.
- Los servicios reciben `db: Database` como primer argumento.
- Las fechas se guardan en SQLite como texto `'YYYY-MM-DD HH:MM:SS'`.
  SQLite no tiene tipo fecha: **toda comparacion de fechas es comparacion de cadenas.**

## Tests

- `pytest`, sin mocks. Cada test usa una base SQLite en memoria (fixture `db`).
- Los helpers compartidos viven en `tests/conftest.py`.
- Nombres de test descriptivos y en espanol: `test_reporte_excluye_otros_meses`.
- Todo arreglo de bug entra con un test de regresion que falle antes del cambio.

## Al trabajar en este repo

- Antes de tocar codigo, reproduce el problema con un test que falle.
- No modifiques tests existentes para que pasen: si un test estorba, explica por que.
- Corre la suite completa antes de dar por terminado un cambio.
