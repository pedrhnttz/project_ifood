from flask import Blueprint, render_template, request, redirect, url_for
from src.models.restaurante import RestauranteModel

restaurantes_bp = Blueprint('restaurantes', __name__)

@restaurantes_bp.route('/', methods=['GET'])
def listar():
    restaurantes = RestauranteModel.listar_todos()
    return render_template('restaurantes/index.html', restaurantes=restaurantes)

@restaurantes_bp.route('/novo', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        taxa = request.form['taxa_entrega']
        
        RestauranteModel.criar(nome, categoria, endereco, telefone, taxa)
        return redirect(url_for('restaurantes.listar'))
        
    return render_template('restaurantes/form.html', restaurante=None)

@restaurantes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    restaurante = RestauranteModel.buscar_por_id(id)
    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        taxa = request.form['taxa_entrega']
        
        RestauranteModel.atualizar(id, nome, categoria, endereco, telefone, taxa)
        return redirect(url_for('restaurantes.listar'))
        
    return render_template('restaurantes/form.html', restaurante=restaurante)

@restaurantes_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    RestauranteModel.deletar(id)
    return redirect(url_for('restaurantes.listar'))