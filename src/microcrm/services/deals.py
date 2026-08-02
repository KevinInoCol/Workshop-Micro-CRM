"""Reglas de negocio de oportunidades (deals)."""

from __future__ import annotations

from datetime import datetime

from .. import repository as repo
from ..db import Database
from ..models import ETAPAS_CERRADAS, Deal, Etapa, NoEncontrado


def crear_deal(
    db: Database,
    contacto_id: int,
    titulo: str,
    monto: float,
    etapa: Etapa = Etapa.NUEVO,
) -> Deal:
    if not repo.contacto_por_id(db, contacto_id):
        raise NoEncontrado(f"No existe el contacto {contacto_id}")

    deal = Deal(
        id=None,
        contacto_id=contacto_id,
        titulo=titulo.strip(),
        monto=float(monto),
        etapa=etapa,
        creado_en=datetime.now(),
    )
    return repo.insertar_deal(db, deal)


def obtener_deal(db: Database, deal_id: int) -> Deal:
    deal = repo.deal_por_id(db, deal_id)
    if not deal:
        raise NoEncontrado(f"No existe el deal {deal_id}")
    return deal


def mover_a_etapa(
    db: Database, deal_id: int, nueva_etapa: Etapa, momento: datetime | None = None
) -> Deal:
    """Mueve un deal a otra etapa del pipeline.

    Al entrar a una etapa cerrada (ganado / perdido) se sella `cerrado_en`.
    """
    deal = obtener_deal(db, deal_id)
    momento = momento or datetime.now()

    cerrado_en = momento if nueva_etapa in ETAPAS_CERRADAS else None
    repo.actualizar_etapa_deal(db, deal_id, nueva_etapa, cerrado_en)

    deal.etapa = nueva_etapa
    deal.cerrado_en = cerrado_en
    return deal


def pipeline_abierto(db: Database) -> dict[str, float]:
    """Monto total por etapa, considerando solo deals que siguen abiertos."""
    resumen: dict[str, float] = {etapa.value: 0.0 for etapa in Etapa if etapa not in ETAPAS_CERRADAS}
    for deal in repo.deals_activos(db):
        resumen[deal.etapa.value] += deal.monto
    return resumen
