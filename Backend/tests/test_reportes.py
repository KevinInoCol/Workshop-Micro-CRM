"""Tests de reportes comerciales."""

from __future__ import annotations

from datetime import datetime

from microcrm.models import Etapa
from microcrm.services import reportes as svc

from .conftest import crear_deal_cerrado


def test_reporte_cuenta_ganados_y_perdidos(db, contacto):
    crear_deal_cerrado(db, contacto.id, "A", 10_000, Etapa.GANADO, datetime(2026, 3, 10, 9, 0))
    crear_deal_cerrado(db, contacto.id, "B", 4_000, Etapa.PERDIDO, datetime(2026, 3, 12, 16, 0))

    reporte = svc.reporte_mensual(db, 2026, 3)

    assert reporte.deals_ganados == 1
    assert reporte.deals_perdidos == 1
    assert reporte.monto_ganado == 10_000
    assert reporte.tasa_conversion == 0.5


def test_reporte_excluye_otros_meses(db, contacto):
    crear_deal_cerrado(db, contacto.id, "Marzo", 10_000, Etapa.GANADO, datetime(2026, 3, 10, 9, 0))
    crear_deal_cerrado(db, contacto.id, "Abril", 99_000, Etapa.GANADO, datetime(2026, 4, 2, 9, 0))

    reporte = svc.reporte_mensual(db, 2026, 3)

    assert reporte.deals_ganados == 1
    assert reporte.monto_ganado == 10_000


def test_reporte_incluye_el_primer_dia_del_mes(db, contacto):
    crear_deal_cerrado(db, contacto.id, "Dia 1", 7_000, Etapa.GANADO, datetime(2026, 3, 1, 8, 30))

    reporte = svc.reporte_mensual(db, 2026, 3)

    assert reporte.deals_ganados == 1
    assert reporte.monto_ganado == 7_000


def test_reporte_sin_cierres_no_divide_por_cero(db):
    reporte = svc.reporte_mensual(db, 2026, 3)

    assert reporte.deals_ganados == 0
    assert reporte.tasa_conversion == 0.0
