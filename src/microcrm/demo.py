"""Datos de ejemplo para la demo.

No forma parte del dominio: existe solo para que la interfaz tenga algo
que mostrar sin tener que cargar todo a mano.
"""

from __future__ import annotations

from datetime import datetime

from . import repository as repo
from .db import Database
from .models import Contacto, Deal, Etapa

CONTACTOS = [
    ("Ana Torres", "ana@acme.pe", "ACME Peru"),
    ("Luis Vera", "luis@nova.pe", "Nova Digital"),
    ("Marta Rios", "marta@delta.pe", "Delta Consulting"),
    ("Pedro Salas", "pedro@zeta.pe", "Zeta Retail"),
]

# (contacto, titulo, monto, etapa, cerrado_en)
DEALS = [
    # --- Cerrados en marzo 2026 -------------------------------------------
    (1, "Licencias Q1", 8_000, Etapa.GANADO, datetime(2026, 3, 10, 11, 0)),
    (2, "Migracion CRM", 25_000, Etapa.GANADO, datetime(2026, 3, 31, 17, 45)),
    (3, "Soporte anual", 15_000, Etapa.GANADO, datetime(2026, 3, 31, 18, 20)),
    (4, "Piloto retail", 6_000, Etapa.PERDIDO, datetime(2026, 3, 22, 9, 30)),
    # --- Cerrados en febrero 2026 -----------------------------------------
    (1, "Consultoria inicial", 10_000, Etapa.GANADO, datetime(2026, 2, 28, 16, 0)),
    (2, "Capacitacion equipo", 4_500, Etapa.GANADO, datetime(2026, 2, 14, 10, 0)),
    # --- Abiertos ----------------------------------------------------------
    (1, "Ampliacion licencias", 18_000, Etapa.NEGOCIACION, None),
    (2, "Modulo facturacion", 12_000, Etapa.PROPUESTA, None),
    (3, "Integracion WhatsApp", 9_000, Etapa.CONTACTADO, None),
    (4, "Renovacion 2027", 22_000, Etapa.NUEVO, None),
]


def sembrar(db: Database) -> dict[str, int]:
    """Borra todo y carga el set de datos de la demo."""
    db.ejecutar("DELETE FROM deals")
    db.ejecutar("DELETE FROM contactos")
    db.ejecutar("DELETE FROM sqlite_sequence WHERE name IN ('deals', 'contactos')")

    for nombre, email, empresa in CONTACTOS:
        repo.insertar_contacto(
            db,
            Contacto(
                id=None,
                nombre=nombre,
                email=email,
                empresa=empresa,
                creado_en=datetime(2026, 1, 15, 9, 0),
            ),
        )

    for contacto_id, titulo, monto, etapa, cerrado_en in DEALS:
        repo.insertar_deal(
            db,
            Deal(
                id=None,
                contacto_id=contacto_id,
                titulo=titulo,
                monto=monto,
                etapa=etapa,
                creado_en=datetime(2026, 1, 20, 9, 0),
                cerrado_en=cerrado_en,
            ),
        )

    return {"contactos": len(CONTACTOS), "deals": len(DEALS)}
