from flask import Blueprint

restaurantes_bp = Blueprint('restaurantes', __name__)

@restaurantes_bp.route('/', methods=['GET'])
def listar():
    pass

@restaurantes_bp.route('/novo', methods=['GET', 'POST'])
def criar():
    pass

@restaurantes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pass

@restaurantes_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    pass