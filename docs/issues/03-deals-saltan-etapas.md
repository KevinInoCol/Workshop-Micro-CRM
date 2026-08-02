---
titulo: "Un deal puede saltarse etapas del pipeline y hasta reabrirse"
etiquetas: bug, reglas-de-negocio
uso: laboratorio (bloque 3)
---

## Que pasa

El pipeline se supone que es un embudo:

```
nuevo -> contactado -> propuesta -> negociacion -> ganado
                                                \-> perdido
```

Pero el sistema deja mover un deal a cualquier etapa desde cualquier otra.

## Como reproducirlo

**Caso A — saltarse el embudo completo**

1. Cargar los datos de ejemplo
2. En Pipeline, buscar "Renovacion 2027" (esta en `nuevo`)
3. Cambiar el select directamente a `ganado`

Queda ganado sin haber pasado por contactado, propuesta ni negociacion. En el
reporte de este mes aparece como venta cerrada.

**Caso B — reabrir algo ya cerrado**

1. Tomar cualquier deal en `ganado` (por ejemplo "Migracion CRM")
2. Cambiarlo a `nuevo`

Vuelve al pipeline abierto y pierde su fecha de cierre. La venta desaparece del
historico del mes en que se cerro.

## Que esperaria

- Un deal avanza de a una etapa por vez dentro del embudo.
- Desde cualquier etapa activa se puede cerrar como `ganado` o `perdido`
  (eso si es valido: una venta se puede perder en cualquier momento).
- Un deal ya cerrado **no** se reabre. Si de verdad hace falta corregir un
  cierre equivocado, que sea una operacion explicita y no un cambio de select.

## Cuanto importa

El caso B es el grave: nos borra ventas del historico. Ya nos paso una vez que
un reporte de un mes cerrado cambio de cifras semanas despues, y nadie supo
explicar por que.
