import sqlite3
from pathlib import Path

DB_NAME = "Instal_Electric.db"
DB_PATH = Path(__file__).parent / DB_NAME


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


AUDITORIA = """
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uuid TEXT UNIQUE NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    created_by TEXT,
    updated_by TEXT,
    status TEXT DEFAULT 'ativo',
    observacoes TEXT
"""


def criar_banco():
    conn = conectar()
    cursor = conn.cursor()

    cursor.executescript("""
    DROP TABLE IF EXISTS sincronizacao;
    DROP TABLE IF EXISTS configuracoes;
    DROP TABLE IF EXISTS usuarios;
    DROP TABLE IF EXISTS eventos;
    DROP TABLE IF EXISTS inspecoes;
    DROP TABLE IF EXISTS manutencoes;
    DROP TABLE IF EXISTS marcadores;
    DROP TABLE IF EXISTS plantas;
    DROP TABLE IF EXISTS arquivos_dxf;
    DROP TABLE IF EXISTS arquivos_ifc;
    DROP TABLE IF EXISTS modelos3d;
    DROP TABLE IF EXISTS fotos360;
    DROP TABLE IF EXISTS documentos;
    DROP TABLE IF EXISTS equipamentos;
    DROP TABLE IF EXISTS circuitos;
    DROP TABLE IF EXISTS quadros;
    DROP TABLE IF EXISTS ambientes;
    DROP TABLE IF EXISTS setores;
    DROP TABLE IF EXISTS pavimentos;
    DROP TABLE IF EXISTS edificios;
    """)

    cursor.executescript(f"""
    CREATE TABLE edificios (
        {AUDITORIA},
        codigo TEXT UNIQUE NOT NULL,
        nome TEXT NOT NULL,
        endereco TEXT
    );

    CREATE TABLE pavimentos (
        {AUDITORIA},
        edificio_id INTEGER NOT NULL,
        codigo TEXT NOT NULL,
        nome TEXT NOT NULL,
        nivel INTEGER,
        FOREIGN KEY (edificio_id) REFERENCES edificios(id)
    );

    CREATE TABLE setores (
        {AUDITORIA},
        pavimento_id INTEGER NOT NULL,
        codigo TEXT NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        FOREIGN KEY (pavimento_id) REFERENCES pavimentos(id)
    );

    CREATE TABLE ambientes (
        {AUDITORIA},
        setor_id INTEGER NOT NULL,
        codigo TEXT NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        FOREIGN KEY (setor_id) REFERENCES setores(id)
    );

    CREATE TABLE quadros (
        {AUDITORIA},
        ambiente_id INTEGER NOT NULL,
        codigo TEXT NOT NULL,
        nome TEXT,
        tipo TEXT,
        tensao TEXT,
        fabricante TEXT,
        modelo TEXT,
        FOREIGN KEY (ambiente_id) REFERENCES ambientes(id)
    );

    CREATE TABLE circuitos (
        {AUDITORIA},
        quadro_id INTEGER NOT NULL,
        codigo TEXT NOT NULL,
        nome TEXT,
        descricao TEXT,
        tipo TEXT,
        disjuntor TEXT,
        corrente_a REAL,
        carga_w REAL,
        FOREIGN KEY (quadro_id) REFERENCES quadros(id)
    );

    CREATE TABLE equipamentos (
        {AUDITORIA},
        quadro_id INTEGER,
        circuito_id INTEGER,
        codigo TEXT NOT NULL,
        nome TEXT NOT NULL,
        tipo TEXT,
        fabricante TEXT,
        modelo TEXT,
        potencia TEXT,
        FOREIGN KEY (quadro_id) REFERENCES quadros(id),
        FOREIGN KEY (circuito_id) REFERENCES circuitos(id)
    );

    CREATE TABLE documentos (
        {AUDITORIA},
        quadro_id INTEGER,
        equipamento_id INTEGER,
        codigo TEXT,
        nome TEXT NOT NULL,
        tipo TEXT,
        extensao TEXT,
        versao TEXT,
        url TEXT,
        FOREIGN KEY (quadro_id) REFERENCES quadros(id),
        FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
    );

    CREATE TABLE fotos360 (
        {AUDITORIA},
        ambiente_id INTEGER,
        quadro_id INTEGER,
        codigo TEXT,
        nome TEXT NOT NULL,
        url TEXT NOT NULL,
        FOREIGN KEY (ambiente_id) REFERENCES ambientes(id),
        FOREIGN KEY (quadro_id) REFERENCES quadros(id)
    );

    CREATE TABLE modelos3d (
        {AUDITORIA},
        quadro_id INTEGER,
        equipamento_id INTEGER,
        codigo TEXT,
        nome TEXT NOT NULL,
        formato TEXT,
        versao TEXT,
        url TEXT,
        FOREIGN KEY (quadro_id) REFERENCES quadros(id),
        FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
    );

    CREATE TABLE arquivos_ifc (
        {AUDITORIA},
        edificio_id INTEGER,
        codigo TEXT,
        nome TEXT NOT NULL,
        versao TEXT,
        url TEXT,
        FOREIGN KEY (edificio_id) REFERENCES edificios(id)
    );

    CREATE TABLE arquivos_dxf (
        {AUDITORIA},
        pavimento_id INTEGER,
        codigo TEXT,
        nome TEXT NOT NULL,
        versao TEXT,
        url TEXT,
        FOREIGN KEY (pavimento_id) REFERENCES pavimentos(id)
    );

    CREATE TABLE plantas (
        {AUDITORIA},
        pavimento_id INTEGER NOT NULL,
        codigo TEXT,
        nome TEXT NOT NULL,
        formato TEXT,
        escala TEXT,
        url TEXT,
        FOREIGN KEY (pavimento_id) REFERENCES pavimentos(id)
    );

    CREATE TABLE marcadores (
        {AUDITORIA},
        planta_id INTEGER,
        quadro_id INTEGER,
        ambiente_id INTEGER,
        codigo TEXT,
        nome TEXT,
        pos_x REAL,
        pos_y REAL,
        pos_z REAL,
        FOREIGN KEY (planta_id) REFERENCES plantas(id),
        FOREIGN KEY (quadro_id) REFERENCES quadros(id),
        FOREIGN KEY (ambiente_id) REFERENCES ambientes(id)
    );

    CREATE TABLE manutencoes (
        {AUDITORIA},
        quadro_id INTEGER,
        equipamento_id INTEGER,
        codigo TEXT,
        nome TEXT,
        data_evento TEXT,
        descricao TEXT,
        responsavel TEXT,
        FOREIGN KEY (quadro_id) REFERENCES quadros(id),
        FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
    );

    CREATE TABLE inspecoes (
        {AUDITORIA},
        quadro_id INTEGER,
        codigo TEXT,
        nome TEXT,
        data_evento TEXT,
        resultado TEXT,
        responsavel TEXT,
        FOREIGN KEY (quadro_id) REFERENCES quadros(id)
    );

    CREATE TABLE eventos (
        {AUDITORIA},
        quadro_id INTEGER,
        codigo TEXT,
        nome TEXT,
        tipo TEXT,
        data_evento TEXT,
        descricao TEXT,
        usuario TEXT,
        FOREIGN KEY (quadro_id) REFERENCES quadros(id)
    );

    CREATE TABLE usuarios (
        {AUDITORIA},
        codigo TEXT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE,
        perfil TEXT
    );

    CREATE TABLE configuracoes (
        {AUDITORIA},
        chave TEXT UNIQUE NOT NULL,
        valor TEXT,
        descricao TEXT
    );

    CREATE TABLE sincronizacao (
        {AUDITORIA},
        origem TEXT,
        destino TEXT,
        data_sincronizacao TEXT,
        resultado TEXT,
        descricao TEXT
    );
    """)

    conn.commit()
    conn.close()
    print(f"Banco recriado com sucesso: {DB_PATH}")


if __name__ == "__main__":
    criar_banco()