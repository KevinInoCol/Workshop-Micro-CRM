---
titulo: "El reporte mensual no cuadra con el pipeline"
etiquetas: bug, comercial
uso: demo guiada (bloque 1)
---

## Que pasa

Estoy cerrando el reporte de **marzo 2026** para la reunion de directorio y los
numeros no me cuadran.

En la pantalla de Pipeline veo tres oportunidades ganadas en marzo:

| Oportunidad | Cerrada | Monto |
|---|---|---|
| Licencias Q1 | 10/03/2026 | S/ 8,000 |
| Migracion CRM | 31/03/2026 | S/ 25,000 |
| Soporte anual | 31/03/2026 | S/ 15,000 |

Pero arriba, el reporte de marzo dice **1 ganado** y **S/ 8,000**.

Faltan S/ 40,000.

## Como reproducirlo

1. Levantar el proyecto y darle a "Cargar datos de ejemplo"
2. En el reporte, elegir **Marzo / 2026**
3. Comparar la cifra "Ganados" con la tabla de Pipeline de la derecha

La misma diferencia sale por API:

```
GET /reportes/mensual?anio=2026&mes=3
{"deals_ganados": 1, "monto_ganado": 8000.0, ...}
```

## Que esperaria

Que el reporte de marzo cuente los tres deals ganados en marzo: **3 ganados,
S/ 48,000**.

## Cuanto importa

El reporte mensual es lo que se presenta a directorio y lo que alimenta el
calculo de comisiones del equipo comercial. Si sub-reporta, pagamos comisiones
de menos y tomamos decisiones con cifras equivocadas.

Note que **febrero tambien se ve raro**, pero no lo he revisado a fondo.
