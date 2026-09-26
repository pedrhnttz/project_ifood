from src.db import get_db

class PedidoModel:
    @staticmethod
    def criar_pedido(usuario_id, restaurante_id, endereco_entrega, total, itens):
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(
            """
            INSERT INTO pedidos (usuario_id, restaurante_id, status, valor_total, endereco_entrega)
            VALUES (?, ?, 'Pendente', ?, ?)
            """,
            (usuario_id, restaurante_id, total, endereco_entrega)
        )
        pedido_id = cursor.lastrowid

        for refeicao_id, quantidade, preco_unitario in itens:
            cursor.execute(
                """
                INSERT INTO itens_pedido (pedido_id, refeicao_id, quantidade, preco_unitario)
                VALUES (?, ?, ?, ?)
                """,
                (pedido_id, refeicao_id, quantidade, preco_unitario)
            )

        db.commit()
        return pedido_id

    @staticmethod
    def listar_por_usuario(usuario_id):
        db = get_db()
        return db.execute(
            """
            SELECT p.*, r.nome as restaurante_nome 
            FROM pedidos p
            JOIN restaurantes r ON p.restaurante_id = r.id
            WHERE p.usuario_id = ?
            ORDER BY p.criado_em DESC
            """,
            (usuario_id,)
        ).fetchall()

    @staticmethod
    def buscar_por_id(pedido_id):
        db = get_db()
        pedido = db.execute(
            """
            SELECT p.*, r.nome as restaurante_nome 
            FROM pedidos p
            JOIN restaurantes r ON p.restaurante_id = r.id
            WHERE p.id = ?
            """,
            (pedido_id,)
        ).fetchone()

        if not pedido:
            return None

        itens = db.execute(
            """
            SELECT ip.*, ref.nome as refeicao_nome 
            FROM itens_pedido ip
            JOIN refeicoes ref ON ip.refeicao_id = ref.id
            WHERE ip.pedido_id = ?
            """,
            (pedido_id,)
        ).fetchall()

        return {'pedido': pedido, 'itens': itens}