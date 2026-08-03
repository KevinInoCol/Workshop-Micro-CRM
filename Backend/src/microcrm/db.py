"""Conexion SQLite y esquema del Micro-CRM.

Las fechas se guardan como texto ISO con segundos: 'YYYY-MM-DD HH:MM:SS'.
SQLite no tiene tipo fecha nativo, asi que las comparaciones son
comparaciones de cadena. Tenlo presente al escribir filtros por rango.
"""

from __future__ import annotations

import sqlite3

ESQUEMA = """
CREATE TABLE IF NOT EXISTS contactos (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre     TEXT NOT NULL,
    email      TEXT NOT NULL,
    empresa    TEXT,
    creado_en  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS deals (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    contacto_id INTEGER NOT NULL REFERENCES contactos(id),
    titulo      TEXT NOT NULL,
    monto       REAL NOT NULL DEFAULT 0,
    etapa       TEXT NOT NULL,
    creado_en   TEXT NOT NULL,
    cerrado_en  TEXT
);

CREATE INDEX IF NOT EXISTS idx_deals_cerrado_en ON deals(cerrado_en);
CREATE INDEX IF NOT EXISTS idx_deals_etapa      ON deals(etapa);
"""

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"


class Database:
    """Envoltorio delgado sobre sqlite3 con el esquema ya aplicado."""

    def __init__(self, ruta: str = ":memory:") -> None:
        self.conn = sqlite3.connect(ruta, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(ESQUEMA)
        self.conn.commit()

    def ejecutar(self, sql: str, parametros: tuple = ()) -> sqlite3.Cursor:
        cur = self.conn.execute(sql, parametros)
        self.conn.commit()
        return cur

    def consultar(self, sql: str, parametros: tuple = ()) -> list[sqlite3.Row]:
        return self.conn.execute(sql, parametros).fetchall()

    def consultar_uno(self, sql: str, parametros: tuple = ()) -> sqlite3.Row | None:
        return self.conn.execute(sql, parametros).fetchone()

    def cerrar(self) -> None:
        self.conn.close()
