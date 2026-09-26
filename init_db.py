import sqlite3
import os

os.makedirs('db', exist_ok=True)

conn = sqlite3.connect('../db/db.sqlite')
cursor = conn.cursor()

with open('../db/script.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

cursor.executescript(sql_script)
conn.commit()
conn.close()

print("Banco de dados criado e tabelas inicializadas com sucesso!")