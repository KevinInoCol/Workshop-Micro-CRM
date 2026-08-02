"""Tests de la capa de contactos."""

from __future__ import annotations

import pytest

from microcrm.models import ContactoDuplicado, NoEncontrado
from microcrm.services import contactos as svc

from .conftest import insertar_contacto_crudo


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


def test_email_duplicado_con_otra_capitalizacion_es_rechazado(db):
    svc.crear_contacto(db, "Luis Vera", "luis@nova.pe", "Nova Digital")
    with pytest.raises(ContactoDuplicado):
        svc.crear_contacto(db, "Luis V.", "LUIS@nova.pe", "Nova Digital")


def test_email_duplicado_con_espacios_alrededor_es_rechazado(db):
    svc.crear_contacto(db, "Luis Vera", "luis@nova.pe")
    with pytest.raises(ContactoDuplicado):
        svc.crear_contacto(db, "Luis V.", "  Luis@Nova.pe  ")


def test_email_se_guarda_en_minusculas(db):
    contacto = svc.crear_contacto(db, "Luis V.", "  LUIS@Nova.PE  ")
    assert contacto.email == "luis@nova.pe"


def test_email_duplicado_detecta_filas_previas_en_mayusculas(db):
    """Las filas ya guardadas con mayusculas tambien bloquean el duplicado."""
    insertar_contacto_crudo(db, "Luis V.", "LUIS@nova.pe", "Nova Digital")
    with pytest.raises(ContactoDuplicado):
        svc.crear_contacto(db, "Luis Vera", "luis@nova.pe", "Nova Digital")


def test_emails_distintos_no_se_confunden(db):
    svc.crear_contacto(db, "Luis Vera", "luis@nova.pe")
    otro = svc.crear_contacto(db, "Ana Torres", "ana@nova.pe")
    assert otro.id is not None


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
