"""Tests de la capa de contactos."""

from __future__ import annotations

import pytest

from microcrm.models import ContactoDuplicado, NoEncontrado
from microcrm.services import contactos as svc


def test_crear_contacto_asigna_id(db):
    contacto = svc.crear_contacto(db, "Luis Vera", "luis@nova.pe", "Nova")
    assert contacto.id is not None
    assert contacto.nombre == "Luis Vera"
    assert contacto.empresa == "Nova"


def test_crear_contacto_recorta_espacios(db):
    contacto = svc.crear_contacto(db, "  Luis Vera  ", "luis@nova.pe")
    assert contacto.nombre == "Luis Vera"


def test_email_duplicado_exacto_es_rechazado(db):
    svc.crear_contacto(db, "Luis Vera", "luis@nova.pe")
    with pytest.raises(ContactoDuplicado):
        svc.crear_contacto(db, "Luis V.", "luis@nova.pe")


def test_obtener_contacto_inexistente(db):
    with pytest.raises(NoEncontrado):
        svc.obtener_contacto(db, 9999)


def test_buscar_por_nombre_parcial(db):
    svc.crear_contacto(db, "Ana Torres", "ana@acme.pe", "ACME")
    svc.crear_contacto(db, "Luis Vera", "luis@nova.pe", "Nova")

    resultados = svc.buscar(db, "Ana")
    assert [c.nombre for c in resultados] == ["Ana Torres"]


def test_buscar_por_empresa(db):
    svc.crear_contacto(db, "Ana Torres", "ana@acme.pe", "ACME")
    svc.crear_contacto(db, "Luis Vera", "luis@nova.pe", "Nova")

    resultados = svc.buscar(db, "Nova")
    assert [c.nombre for c in resultados] == ["Luis Vera"]


def test_buscar_sin_termino_devuelve_todo(db):
    svc.crear_contacto(db, "Ana Torres", "ana@acme.pe", "ACME")
    svc.crear_contacto(db, "Luis Vera", "luis@nova.pe", "Nova")

    assert len(svc.buscar(db, "  ")) == 2
