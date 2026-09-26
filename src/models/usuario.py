from src.db import get_db

class UsuarioModel:
    @staticmethod
    def buscar_por_email(email):
        db = get_db()
        return db.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()

    @staticmethod
    def buscar_por_id(id):
        db = get_db()
        return db.execute("SELECT * FROM usuarios WHERE id = ?", (id,)).fetchone()

    @staticmethod
    def criar_ou_atualizar(nome, email, google_id, foto=None):
        db = get_db()
        
        usuario = db.execute(
            "SELECT * FROM usuarios WHERE email = ? OR oauth_id = ?", 
            (email, google_id)
        ).fetchone()

        if usuario:
            db.execute(
                "UPDATE usuarios SET nome = ?, oauth_id = ?, provedor_oauth = 'google' WHERE id = ?",
                (nome, google_id, usuario['id'])
            )
        else:
            db.execute(
                "INSERT INTO usuarios (nome, email, provedor_oauth, oauth_id) VALUES (?, ?, 'google', ?)",
                (nome, email, google_id)
            )
        db.commit()
        return db.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()