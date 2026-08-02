"""Tests de la capa de oportunidades."""

from __future__ import annotations

from datetime import datetime

import pytest

from microcrm.models import Etapa, NoEncontrado
from microcrm.services import deals as svc


def test_crear_deal_arranca_en_nuevo(db, contacto):
    deal = svc.crear_deal(db, contacto.id, "Licencias 2026", 12_000)
    assert deal.etapa == Etapa.NUEVO
    assert deal.cerrado_en is None


def test_crear_deal_con_contacto_inexistente(db):
    with pytest.raises(NoEncontrado):
        svc.crear_deal(db, 9999, "Fantasma", 100)


def test_avanzar_una_etapa(db, contacto):
    deal = svc.crear_deal(db, contacto.id, "Licencias 2026", 12_000)
    movido = svc.mover_a_etapa(db, deal.id, Etapa.CONTACTADO)
    assert movido.etapa == Etapa.CONTACTADO
    assert movido.cerrado_en is None


def test_ganar_deal_sella_fecha_de_cierre(db, contacto):
    deal = svc.crear_deal(db, contacto.id, "Licencias 2026", 12_000)
    momento = datetime(2026, 3, 15, 11, 30, 0)

    ganado = svc.mover_a_etapa(db, deal.id, Etapa.GANADO, momento=momento)

    assert ganado.etapa == Etapa.GANADO
    assert ganado.cerrado_en == momento


def test_pipeline_abierto_ignora_cerrados(db, contacto):
    abierto = svc.crear_deal(db, contacto.id, "Abierto", 5_000)
    svc.mover_a_etapa(db, abierto.id, Etapa.PROPUESTA)

    cerrado = svc.crear_deal(db, contacto.id, "Cerrado", 9_000)
    svc.mover_a_etapa(db, cerrado.id, Etapa.GANADO)

    resumen = svc.pipeline_abierto(db)

    assert resumen["propuesta"] == 5_000
    assert "ganado" not in resumen
    assert sum(resumen.values()) == 5_000
