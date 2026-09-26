from flask import Blueprint

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
def listar():
    pass

@usuarios_bp.route('/novo', methods=['GET', 'POST'])
def criar():
    pass

@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    pass

@usuarios_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    pass