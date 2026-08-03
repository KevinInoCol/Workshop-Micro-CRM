"""Fixtures compartidas de la suite."""

from __future__ import annotations

from datetime import datetime

import pytest

from microcrm.db import Database
from microcrm.models import Contacto, Deal, Etapa
from microcrm.repository import insertar_contacto, insertar_deal


@pytest.fixture
def db() -> Database:
    """Base de datos limpia en memoria para cada test."""
    base = Database(":memory:")
    yield base
    base.cerrar()


@pytest.fixture
def contacto(db: Database) -> Contacto:
    return insertar_contacto(
        db,
        Contacto(
            id=None,
            nombre="Ana Torres",
            email="ana@acme.pe",
            empresa="ACME",
            creado_en=datetime(2026, 1, 5, 9, 0, 0),
        ),
    )


def crear_deal_cerrado(
    db: Database,
    contacto_id: int,
    titulo: str,
    monto: float,
    etapa: Etapa,
    cerrado_en: datetime,
) -> Deal:
    """Helper para sembrar deals ya cerrados con una fecha exacta."""
    return insertar_deal(
        db,
        Deal(
            id=None,
            contacto_id=contacto_id,
            titulo=titulo,
            monto=monto,
            etapa=etapa,
            creado_en=datetime(cerrado_en.year, cerrado_en.month, 1, 8, 0, 0),
            cerrado_en=cerrado_en,
        ),
    )
