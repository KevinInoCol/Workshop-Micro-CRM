"""Acceso a datos. Toda consulta SQL vive aqui; los servicios nunca escriben SQL."""

from __future__ import annotations

from datetime import datetime

from .db import FORMATO_FECHA, Database
from .models import Contacto, Deal, Etapa


def _a_contacto(fila) -> Contacto:
    return Contacto(
        id=fila["id"],
        nombre=fila["nombre"],
        email=fila["email"],
        empresa=fila["empresa"],
        creado_en=datetime.strptime(fila["creado_en"], FORMATO_FECHA),
    )


def _a_deal(fila) -> Deal:
    return Deal(
        id=fila["id"],
        contacto_id=fila["contacto_id"],
        titulo=fila["titulo"],
        monto=fila["monto"],
        etapa=Etapa(fila["etapa"]),
        creado_en=datetime.strptime(fila["creado_en"], FORMATO_FECHA),
        cerrado_en=(
            datetime.strptime(fila["cerrado_en"], FORMATO_FECHA) if fila["cerrado_en"] else None
        ),
    )


# --------------------------------------------------------------------------- contactos


def insertar_contacto(db: Database, contacto: Contacto) -> Contacto:
    cur = db.ejecutar(
        "INSERT INTO contactos (nombre, email, empresa, creado_en) VALUES (?, ?, ?, ?)",
        (
            contacto.nombre,
            contacto.email,
            contacto.empresa,
            (contacto.creado_en or datetime.now()).strftime(FORMATO_FECHA),
        ),
    )
    contacto.id = cur.lastrowid
    return contacto


def contacto_por_id(db: Database, contacto_id: int) -> Contacto | None:
    fila = db.consultar_uno("SELECT * FROM contactos WHERE id = ?", (contacto_id,))
    return _a_contacto(fila) if fila else None


def contacto_por_email(db: Database, email: str) -> Contacto | None:
    fila = db.consultar_uno(
        "SELECT * FROM contactos WHERE email = ? COLLATE NOCASE", (email,)
    )
    return _a_contacto(fila) if fila else None


def buscar_contactos(db: Database, termino: str) -> list[Contacto]:
    """Busca por coincidencia parcial en nombre o empresa."""
    patron = f"%{termino}%"
    filas = db.consultar(
        "SELECT * FROM contactos WHERE nombre LIKE ? OR empresa LIKE ? ORDER BY nombre",
        (patron, patron),
    )
    return [_a_contacto(f) for f in filas]


def listar_contactos(db: Database) -> list[Contacto]:
    return [_a_contacto(f) for f in db.consultar("SELECT * FROM contactos ORDER BY nombre")]


# ------------------------------------------------------------------------------- deals


def insertar_deal(db: Database, deal: Deal) -> Deal:
    cur = db.ejecutar(
        """INSERT INTO deals (contacto_id, titulo, monto, etapa, creado_en, cerrado_en)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            deal.contacto_id,
            deal.titulo,
            deal.monto,
            deal.etapa.value,
            (deal.creado_en or datetime.now()).strftime(FORMATO_FECHA),
            deal.cerrado_en.strftime(FORMATO_FECHA) if deal.cerrado_en else None,
        ),
    )
    deal.id = cur.lastrowid
    return deal


def deal_por_id(db: Database, deal_id: int) -> Deal | None:
    fila = db.consultar_uno("SELECT * FROM deals WHERE id = ?", (deal_id,))
    return _a_deal(fila) if fila else None


def actualizar_etapa_deal(
    db: Database, deal_id: int, etapa: Etapa, cerrado_en: datetime | None
) -> None:
    db.ejecutar(
        "UPDATE deals SET etapa = ?, cerrado_en = ? WHERE id = ?",
        (etapa.value, cerrado_en.strftime(FORMATO_FECHA) if cerrado_en else None, deal_id),
    )


def deals_por_contacto(db: Database, contacto_id: int) -> list[Deal]:
    filas = db.consultar(
        "SELECT * FROM deals WHERE contacto_id = ? ORDER BY creado_en", (contacto_id,)
    )
    return [_a_deal(f) for f in filas]


def listar_deals(db: Database) -> list[Deal]:
    return [_a_deal(f) for f in db.consultar("SELECT * FROM deals ORDER BY id")]


def deals_activos(db: Database) -> list[Deal]:
    filas = db.consultar(
        "SELECT * FROM deals WHERE etapa NOT IN ('ganado', 'perdido') ORDER BY creado_en"
    )
    return [_a_deal(f) for f in filas]


def deals_cerrados_entre(db: Database, desde: str, hasta: str) -> list[Deal]:
    """Deals con fecha de cierre dentro del rango [desde, hasta].

    `desde` y `hasta` son cadenas de fecha en formato ISO.
    """
    filas = db.consultar(
        """SELECT * FROM deals
           WHERE cerrado_en IS NOT NULL
             AND cerrado_en >= ?
             AND cerrado_en <= ?
           ORDER BY cerrado_en""",
        (desde, hasta),
    )
    return [_a_deal(f) for f in filas]
