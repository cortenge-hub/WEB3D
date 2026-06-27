from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)

DB_PATH = Path(__file__).parent / "Instal_Electric.db"


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@app.route("/")
def home():
    return "API SQLite funcionando."


@app.route("/edificios", methods=["GET"])
def listar_edificios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM edificios ORDER BY id DESC")
    dados = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return jsonify(dados)


@app.route("/edificios", methods=["POST"])
def criar_edificio():
    dados = request.json

    codigo = dados.get("codigo")
    nome = dados.get("nome")
    endereco = dados.get("endereco")
    observacoes = dados.get("observacoes")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO edificios (codigo, nome, endereco, observacoes)
        VALUES (?, ?, ?, ?)
    """, (codigo, nome, endereco, observacoes))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Edifício cadastrado com sucesso"})


@app.route("/edificios/<int:id>", methods=["DELETE"])
def excluir_edificio(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM edificios WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Edifício excluído com sucesso"})


if __name__ == "__main__":
    app.run(debug=True)
