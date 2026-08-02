---
titulo: "Se crean contactos duplicados cuando el email cambia de mayusculas"
etiquetas: bug, datos
uso: demo de @claude en GitHub Actions (bloque 2)
---

## Que pasa

Tenemos la misma persona cargada dos veces. El sistema deberia impedirlo —de
hecho lo impide si escribes el email identico— pero basta cambiar una mayuscula
para que lo deje pasar.

## Como reproducirlo

1. Cargar los datos de ejemplo
2. En Contactos, agregar:
   - Nombre: `Luis V.`
   - Email: `LUIS@nova.pe`
   - Empresa: `Nova Digital`
3. Buscar "Nova"

Aparecen dos filas:

```
Luis V.     LUIS@nova.pe    Nova Digital
Luis Vera   luis@nova.pe    Nova Digital
```

Si en el paso 2 escribes `luis@nova.pe` en minusculas, si lo rechaza con
"Ya existe un contacto con el email luis@nova.pe". Solo falla cuando cambia
la capitalizacion.

## Que esperaria

Que los emails se traten sin distinguir mayusculas de minusculas, porque
`LUIS@nova.pe` y `luis@nova.pe` son el mismo buzon. El segundo intento deberia
ser rechazado igual que el primero.

## Cuanto importa

Cada duplicado parte el historial de un cliente en dos fichas. El vendedor ve
media conversacion y llamamos dos veces a la misma persona.

Hoy tenemos ~40 duplicados en produccion por esta causa.
