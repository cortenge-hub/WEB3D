import sqlite3
from pathlib import Path

DB_NAME = "Instal_Electric.db"
DB_PATH = Path(__file__).parent / DB_NAME

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.executescript("""
CREATE TABLE IF NOT EXISTS edificios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    endereco TEXT,
    observacoes TEXT
);

CREATE TABLE IF NOT EXISTS pavimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    edificio_id INTEGER NOT NULL,
    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,
    nivel INTEGER,
    FOREIGN KEY (edificio_id) REFERENCES edificios(id)
);

CREATE TABLE IF NOT EXISTS setores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pavimento_id INTEGER NOT NULL,
    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,
    FOREIGN KEY (pavimento_id) REFERENCES pavimentos(id)
);

CREATE TABLE IF NOT EXISTS ambientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setor_id INTEGER NOT NULL,
    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT,
    FOREIGN KEY (setor_id) REFERENCES setores(id)
);

CREATE TABLE IF NOT EXISTS quadros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ambiente_id INTEGER NOT NULL,
    codigo TEXT NOT NULL,
    nome TEXT,
    tipo TEXT,
    tensao TEXT,
    status TEXT DEFAULT 'ativo',
    FOREIGN KEY (ambiente_id) REFERENCES ambientes(id)
);

CREATE TABLE IF NOT EXISTS circuitos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quadro_id INTEGER NOT NULL,
    codigo TEXT NOT NULL,
    descricao TEXT,
    tipo TEXT,
    disjuntor TEXT,
    carga_w REAL,
    FOREIGN KEY (quadro_id) REFERENCES quadros(id)
);

CREATE TABLE IF NOT EXISTS equipamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    circuito_id INTEGER,
    quadro_id INTEGER,
    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,
    tipo TEXT,
    fabricante TEXT,
    modelo TEXT,
    potencia TEXT,
    FOREIGN KEY (circuito_id) REFERENCES circuitos(id),
    FOREIGN KEY (quadro_id) REFERENCES quadros(id)
);

CREATE TABLE IF NOT EXISTS documentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quadro_id INTEGER,
    equipamento_id INTEGER,
    nome TEXT NOT NULL,
    tipo TEXT,
    link TEXT,
    observacoes TEXT,
    FOREIGN KEY (quadro_id) REFERENCES quadros(id),
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
);

CREATE TABLE IF NOT EXISTS fotos360 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ambiente_id INTEGER,
    quadro_id INTEGER,
    nome TEXT NOT NULL,
    link TEXT NOT NULL,
    FOREIGN KEY (ambiente_id) REFERENCES ambientes(id),
    FOREIGN KEY (quadro_id) REFERENCES quadros(id)
);

CREATE TABLE IF NOT EXISTS modelos3d (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quadro_id INTEGER,
    equipamento_id INTEGER,
    nome TEXT NOT NULL,
    arquivo TEXT,
    formato TEXT,
    FOREIGN KEY (quadro_id) REFERENCES quadros(id),
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
);

CREATE TABLE IF NOT EXISTS arquivos_ifc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    edificio_id INTEGER,
    nome TEXT NOT NULL,
    arquivo TEXT,
    versao TEXT,
    FOREIGN KEY (edificio_id) REFERENCES edificios(id)
);

CREATE TABLE IF NOT EXISTS arquivos_dxf (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pavimento_id INTEGER,
    nome TEXT NOT NULL,
    arquivo TEXT,
    versao TEXT,
    FOREIGN KEY (pavimento_id) REFERENCES pavimentos(id)
);

CREATE TABLE IF NOT EXISTS plantas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pavimento_id INTEGER NOT NULL,
    nome TEXT NOT NULL,
    arquivo TEXT,
    formato TEXT,
    escala TEXT,
    FOREIGN KEY (pavimento_id) REFERENCES pavimentos(id)
);

CREATE TABLE IF NOT EXISTS marcadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    planta_id INTEGER,
    quadro_id INTEGER,
    ambiente_id INTEGER,
    pos_x REAL,
    pos_y REAL,
    pos_z REAL,
    descricao TEXT,
    FOREIGN KEY (planta_id) REFERENCES plantas(id),
    FOREIGN KEY (quadro_id) REFERENCES quadros(id),
    FOREIGN KEY (ambiente_id) REFERENCES ambientes(id)
);

CREATE TABLE IF NOT EXISTS manutencoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quadro_id INTEGER,
    equipamento_id INTEGER,
    data TEXT,
    descricao TEXT,
    responsavel TEXT,
    status TEXT,
    FOREIGN KEY (quadro_id) REFERENCES quadros(id),
    FOREIGN KEY (equipamento_id) REFERENCES equipamentos(id)
);

CREATE TABLE IF NOT EXISTS inspecoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quadro_id INTEGER,
    data TEXT,
    resultado TEXT,
    observacoes TEXT,
    responsavel TEXT,
    FOREIGN KEY (quadro_id) REFERENCES quadros(id)
);

CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quadro_id INTEGER,
    tipo TEXT,
    data TEXT,
    descricao TEXT,
    usuario TEXT,
    FOREIGN KEY (quadro_id) REFERENCES quadros(id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE,
    perfil TEXT,
    status TEXT DEFAULT 'ativo'
);

CREATE TABLE IF NOT EXISTS configuracoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave TEXT UNIQUE NOT NULL,
    valor TEXT,
    descricao TEXT
);

CREATE TABLE IF NOT EXISTS sincronizacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origem TEXT,
    destino TEXT,
    data TEXT,
    status TEXT,
    observacoes TEXT
);
""")

conn.commit()
conn.close()

print(f"Banco criado com sucesso: {DB_PATH}")
