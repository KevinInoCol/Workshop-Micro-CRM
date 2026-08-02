"""API HTTP del Micro-CRM."""

from __future__ import annotations

from dataclasses import asdict

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from .db import Database
from .models import ErrorDeDominio, Etapa, NoEncontrado
from .services import contactos as svc_contactos
from .services import deals as svc_deals
from .services import reportes as svc_reportes

app = FastAPI(title="Micro-CRM", version="0.1.0")

_db = Database("microcrm.db")


def obtener_db() -> Database:
    return _db


class ContactoEntrada(BaseModel):
    nombre: str
    email: str
    empresa: str | None = None


class DealEntrada(BaseModel):
    contacto_id: int
    titulo: str
    monto: float = 0.0


class EtapaEntrada(BaseModel):
    etapa: Etapa


def _traducir(error: ErrorDeDominio) -> HTTPException:
    codigo = 404 if isinstance(error, NoEncontrado) else 400
    return HTTPException(status_code=codigo, detail=str(error))


@app.post("/contactos", status_code=201)
def crear_contacto(entrada: ContactoEntrada, db: Database = Depends(obtener_db)):
    try:
        return asdict(svc_contactos.crear_contacto(db, **entrada.model_dump()))
    except ErrorDeDominio as error:
        raise _traducir(error) from error


@app.get("/contactos")
def buscar_contactos(q: str = "", db: Database = Depends(obtener_db)):
    return [asdict(c) for c in svc_contactos.buscar(db, q)]


@app.post("/deals", status_code=201)
def crear_deal(entrada: DealEntrada, db: Database = Depends(obtener_db)):
    try:
        return asdict(svc_deals.crear_deal(db, **entrada.model_dump()))
    except ErrorDeDominio as error:
        raise _traducir(error) from error


@app.patch("/deals/{deal_id}/etapa")
def mover_etapa(deal_id: int, entrada: EtapaEntrada, db: Database = Depends(obtener_db)):
    try:
        return asdict(svc_deals.mover_a_etapa(db, deal_id, entrada.etapa))
    except ErrorDeDominio as error:
        raise _traducir(error) from error


@app.get("/pipeline")
def pipeline(db: Database = Depends(obtener_db)):
    return svc_deals.pipeline_abierto(db)


@app.get("/reportes/mensual")
def reporte_mensual(anio: int, mes: int, db: Database = Depends(obtener_db)):
    return asdict(svc_reportes.reporte_mensual(db, anio, mes))


@app.get("/reportes/comparativa")
def comparativa(anio: int, mes: int, db: Database = Depends(obtener_db)):
    return svc_reportes.comparativa_mensual(db, anio, mes)
