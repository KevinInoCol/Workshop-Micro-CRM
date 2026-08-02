"""Reportes comerciales del Micro-CRM."""

from __future__ import annotations

import calendar
from datetime import date

from .. import repository as repo
from ..db import Database
from ..models import Etapa, ReporteMensual


def _rango_del_mes(anio: int, mes: int) -> tuple[str, str]:
    """Devuelve el rango de fechas que cubre un mes completo."""
    primer_dia = date(anio, mes, 1)
    ultimo_dia = date(anio, mes, calendar.monthrange(anio, mes)[1])
    return primer_dia.isoformat(), ultimo_dia.isoformat()


def reporte_mensual(db: Database, anio: int, mes: int) -> ReporteMensual:
    """Resumen de cierres de un mes: ganados, perdidos, monto y conversion."""
    desde, hasta = _rango_del_mes(anio, mes)
    cerrados = repo.deals_cerrados_entre(db, desde, hasta)

    ganados = [d for d in cerrados if d.etapa == Etapa.GANADO]
    perdidos = [d for d in cerrados if d.etapa == Etapa.PERDIDO]
    total = len(ganados) + len(perdidos)

    return ReporteMensual(
        anio=anio,
        mes=mes,
        deals_ganados=len(ganados),
        deals_perdidos=len(perdidos),
        monto_ganado=sum(d.monto for d in ganados),
        tasa_conversion=(len(ganados) / total) if total else 0.0,
    )


def comparativa_mensual(db: Database, anio: int, mes: int) -> dict[str, float]:
    """Compara el monto ganado del mes contra el mes anterior."""
    actual = reporte_mensual(db, anio, mes)
    anio_previo, mes_previo = (anio - 1, 12) if mes == 1 else (anio, mes - 1)
    previo = reporte_mensual(db, anio_previo, mes_previo)

    variacion = 0.0
    if previo.monto_ganado:
        variacion = (actual.monto_ganado - previo.monto_ganado) / previo.monto_ganado

    return {
        "monto_actual": actual.monto_ganado,
        "monto_previo": previo.monto_ganado,
        "variacion": variacion,
    }
