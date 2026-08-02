"""Reglas de negocio de contactos."""

from __future__ import annotations

from datetime import datetime

from .. import repository as repo
from ..db import Database
from ..models import Contacto, ContactoDuplicado, NoEncontrado


def normalizar_email(email: str) -> str:
    """Forma canonica de un email: sin espacios alrededor y en minusculas.

    `LUIS@nova.pe` y `luis@nova.pe` son el mismo buzon, asi que se guardan
    igual. Normalizar antes de buscar y antes de insertar evita que la misma
    persona entre dos veces solo por como la escribio el vendedor.
    """
    return email.strip().lower()


def crear_contacto(
    db: Database, nombre: str, email: str, empresa: str | None = None
) -> Contacto:
    """Crea un contacto. El email debe ser unico en todo el CRM.

    La unicidad no distingue mayusculas de minusculas.
    """
    email = normalizar_email(email)
    if repo.contacto_por_email(db, email):
        raise ContactoDuplicado(f"Ya existe un contacto con el email {email}")

    contacto = Contacto(
        id=None,
        nombre=nombre.strip(),
        email=email,
        empresa=empresa.strip() if empresa else None,
        creado_en=datetime.now(),
    )
    return repo.insertar_contacto(db, contacto)


def obtener_contacto(db: Database, contacto_id: int) -> Contacto:
    contacto = repo.contacto_por_id(db, contacto_id)
    if not contacto:
        raise NoEncontrado(f"No existe el contacto {contacto_id}")
    return contacto


def buscar(db: Database, termino: str) -> list[Contacto]:
    """Busqueda libre por nombre o empresa."""
    termino = termino.strip()
    if not termino:
        return repo.listar_contactos(db)
    return repo.buscar_contactos(db, termino)
