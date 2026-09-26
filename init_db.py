import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'db')
DB_PATH = os.path.join(DB_DIR, 'db.sqlite')

os.makedirs(DB_DIR, exist_ok=True)

schema_path = os.path.join(DB_DIR, 'script.sql')

if not os.path.exists(schema_path):
    schema_path = os.path.join(BASE_DIR, 'script.sql')

print(f"A criar a base de dados em: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)

with open(schema_path, 'r', encoding='utf-8') as f:
    schema_sql = f.read()

conn.executescript(schema_sql)
conn.close()

print("Base de dados e tabelas criadas com sucesso!")