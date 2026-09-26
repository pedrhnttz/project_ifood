from src.db import get_db

class RestauranteModel:
    @staticmethod
    def listar_todos():
        db = get_db()
        return db.execute("SELECT * FROM restaurantes").fetchall()

    @staticmethod
    def buscar_por_id(id):
        db = get_db()
        return db.execute("SELECT * FROM restaurantes WHERE id = ?", (id,)).fetchone()

    @staticmethod
    def criar(nome, categoria, endereco, telefone, taxa_entrega):
        db = get_db()
        db.execute(
            "INSERT INTO restaurantes (nome, categoria, endereco, telefone, taxa_entrega) VALUES (?, ?, ?, ?, ?)",
            (nome, categoria, endereco, telefone, taxa_entrega)
        )
        db.commit()

    @staticmethod
    def atualizar(id, nome, categoria, endereco, telefone, taxa_entrega):
        db = get_db()
        db.execute(
            "UPDATE restaurantes SET nome = ?, categoria = ?, endereco = ?, telefone = ?, taxa_entrega = ? WHERE id = ?",
            (nome, categoria, endereco, telefone, taxa_entrega, id)
        )
        db.commit()

    @staticmethod
    def deletar(id):
        db = get_db()
        db.execute("DELETE FROM restaurantes WHERE id = ?", (id,))
        db.commit()