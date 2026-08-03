"""Entidades del dominio del Micro-CRM."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class Etapa(StrEnum):
    """Etapas del pipeline comercial."""

    NUEVO = "nuevo"
    CONTACTADO = "contactado"
    PROPUESTA = "propuesta"
    NEGOCIACION = "negociacion"
    GANADO = "ganado"
    PERDIDO = "perdido"


#: Orden del pipeline activo. Un deal avanza de izquierda a derecha.
PIPELINE_ACTIVO: list[Etapa] = [
    Etapa.NUEVO,
    Etapa.CONTACTADO,
    Etapa.PROPUESTA,
    Etapa.NEGOCIACION,
]

#: Etapas terminales: un deal que llega aqui ya no se mueve.
ETAPAS_CERRADAS: set[Etapa] = {Etapa.GANADO, Etapa.PERDIDO}


@dataclass
class Contacto:
    id: int | None
    nombre: str
    email: str
    empresa: str | None = None
    creado_en: datetime | None = None


@dataclass
class Deal:
    id: int | None
    contacto_id: int
    titulo: str
    monto: float
    etapa: Etapa
    creado_en: datetime | None = None
    cerrado_en: datetime | None = None


@dataclass
class ReporteMensual:
    anio: int
    mes: int
    deals_ganados: int
    deals_perdidos: int
    monto_ganado: float
    tasa_conversion: float


class ErrorDeDominio(Exception):
    """Error de negocio. La capa API lo traduce a HTTP 400."""


class ContactoDuplicado(ErrorDeDominio):
    pass


class TransicionInvalida(ErrorDeDominio):
    pass


class NoEncontrado(ErrorDeDominio):
    pass
