from providers.sqlite_provider import SQLiteProvider

db = SQLiteProvider()

print("\n===== TABELAS =====")
print(db.listar_tabelas())

print("\n===== SCHEMA EDIFICIOS =====")
print(db.schema("edificios"))

print("\n===== DADOS EDIFICIOS =====")
print(db.dados("edificios"))
