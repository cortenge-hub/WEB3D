import sqlite3
from pathlib import Path


class SQLiteProvider:

    def __init__(self):
        self.db_path = (
            Path(__file__).parent.parent
            / "database"
            / "Instal_Electric.db"
        )

    def conectar(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def listar_tabelas(self):

        conn = self.conectar()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """)

        tabelas = [row["name"] for row in cursor.fetchall()]

        conn.close()

        return tabelas

    def schema(self, tabela):

        conn = self.conectar()

        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({tabela});")

        colunas = []

        for row in cursor.fetchall():

            colunas.append({
                "name": row["name"],
                "type": row["type"],
                "notnull": row["notnull"],
                "pk": row["pk"]
            })

        conn.close()

        return colunas

    def dados(self, tabela, limite=100):

        conn = self.conectar()

        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT *
            FROM {tabela}
            LIMIT {limite}
        """)

        registros = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return registros
