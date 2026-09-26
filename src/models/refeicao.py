from src.db import get_db

class RefeicaoModel:
    @staticmethod
    def listar_por_restaurante(restaurante_id):
        db = get_db()
        return db.execute(
            "SELECT * FROM refeicoes WHERE restaurante_id = ?", 
            (restaurante_id,)
        ).fetchall()

    @staticmethod
    def buscar_por_id(id):
        db = get_db()
        return db.execute("SELECT * FROM refeicoes WHERE id = ?", (id,)).fetchone()

    @staticmethod
    def criar(restaurante_id, nome, descricao, preco):
        db = get_db()
        db.execute(
            "INSERT INTO refeicoes (restaurante_id, nome, descricao, preco) VALUES (?, ?, ?, ?)",
            (restaurante_id, nome, descricao, preco)
        )
        db.commit()

    @staticmethod
    def atualizar(id, nome, descricao, preco):
        db = get_db()
        db.execute(
            "UPDATE refeicoes SET nome = ?, descricao = ?, preco = ? WHERE id = ?",
            (nome, descricao, preco, id)
        )
        db.commit()

    @staticmethod
    def deletar(id):
        db = get_db()
        db.execute("DELETE FROM refeicoes WHERE id = ?", (id,))
        db.commit()