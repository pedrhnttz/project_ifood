from flask import Blueprint, render_template, request, redirect, url_for
from src.models.refeicao import RefeicaoModel
from src.models.restaurante import RestauranteModel

refeicoes_bp = Blueprint('refeicoes', __name__)

@refeicoes_bp.route('/restaurante/<int:restaurante_id>', methods=['GET'])
def listar_por_restaurante(restaurante_id):
    restaurante = RestauranteModel.buscar_por_id(restaurante_id)
    refeicoes = RefeicaoModel.listar_por_restaurante(restaurante_id)
    return render_template('refeicoes/index.html', restaurante=restaurante, refeicoes=refeicoes)

@refeicoes_bp.route('/novo/<int:restaurante_id>', methods=['GET', 'POST'])
def criar(restaurante_id):
    restaurante = RestauranteModel.buscar_por_id(restaurante_id)
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        
        RefeicaoModel.criar(restaurante_id, nome, descricao, preco)
        return redirect(url_for('refeicoes.listar_por_restaurante', restaurante_id=restaurante_id))
        
    return render_template('refeicoes/form.html', restaurante=restaurante, refeicao=None)

@refeicoes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    refeicao = RefeicaoModel.buscar_por_id(id)
    restaurante = RestauranteModel.buscar_por_id(refeicao['restaurante_id'])
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        
        RefeicaoModel.atualizar(id, nome, descricao, preco)
        return redirect(url_for('refeicoes.listar_por_restaurante', restaurante_id=refeicao['restaurante_id']))
        
    return render_template('refeicoes/form.html', restaurante=restaurante, refeicao=refeicao)

@refeicoes_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    refeicao = RefeicaoModel.buscar_por_id(id)
    restaurante_id = refeicao['restaurante_id']
    RefeicaoModel.deletar(id)
    return redirect(url_for('refeicoes.listar_por_restaurante', restaurante_id=restaurante_id))