from flask import Blueprint

refeicoes_bp = Blueprint('refeicoes', __name__)

@refeicoes_bp.route('/restaurante/<int:restaurante_id>', methods=['GET'])
def listar_por_restaurante(restaurante_id):
    pass

@refeicoes_bp.route('/novo', methods=['GET', 'POST'])
def criar():
    pass

@refeicoes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pass

@refeicoes_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    pass