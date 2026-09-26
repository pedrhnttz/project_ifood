from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from src.models.pedido import PedidoModel
from src.models.refeicao import RefeicaoModel
from src.models.restaurante import RestauranteModel

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/carrinho/adicionar', methods=['POST'])
def adicionar_carrinho():
    refeicao_id = int(request.form['refeicao_id'])
    restaurante_id = int(request.form['restaurante_id'])
    
    refeicao = RefeicaoModel.buscar_por_id(refeicao_id)
    if not refeicao:
        flash('Refeição não encontrada.', 'danger')
        return redirect(url_for('restaurantes.listar'))

    if 'carrinho' not in session:
        session['carrinho'] = {'restaurante_id': restaurante_id, 'itens': {}}

    if session['carrinho'].get('restaurante_id') != restaurante_id:
        session['carrinho'] = {'restaurante_id': restaurante_id, 'itens': {}}
        flash('O carrinho foi reiniciado porque escolheu itens de outro restaurante.', 'warning')

    itens = session['carrinho']['itens']
    str_id = str(refeicao_id)
    if str_id in itens:
        itens[str_id]['quantidade'] += 1
    else:
        itens[str_id] = {
            'id': refeicao['id'],
            'nome': refeicao['nome'],
            'preco': float(refeicao['preco']),
            'quantidade': 1
        }

    session.modified = True
    flash(f"{refeicao['nome']} adicionado ao carrinho!", 'success')
    return redirect(url_for('refeicoes.listar_por_restaurante', restaurante_id=restaurante_id))

@pedidos_bp.route('/carrinho', methods=['GET'])
def ver_carrinho():
    carrinho = session.get('carrinho', {'itens': {}})
    itens = list(carrinho.get('itens', {}).values())
    
    restaurante = None
    taxa_entrega = 0.0
    if carrinho.get('restaurante_id'):
        restaurante = RestauranteModel.buscar_por_id(carrinho['restaurante_id'])
        if restaurante:
            taxa_entrega = float(restaurante['taxa_entrega'])

    subtotal = sum(item['preco'] * item['quantidade'] for item in itens)
    total = subtotal + taxa_entrega

    return render_template(
        'pedidos/carrinho.html',
        itens=itens,
        subtotal=subtotal,
        taxa_entrega=taxa_entrega,
        total=total,
        restaurante=restaurante
    )

@pedidos_bp.route('/finalizar', methods=['POST'])
def finalizar_pedido():
    if 'user' not in session:
        flash('Precisa de iniciar sessão para finalizar a encomenda.', 'warning')
        return redirect(url_for('auth.login'))

    carrinho = session.get('carrinho')
    if not carrinho or not carrinho.get('itens'):
        flash('O seu carrinho está vazio.', 'danger')
        return redirect(url_for('restaurantes.listar'))

    endereco = request.form.get('endereco')
    if not endereco:
        flash('Informe o endereço de entrega.', 'danger')
        return redirect(url_for('pedidos.ver_carrinho'))

    restaurante = RestauranteModel.buscar_por_id(carrinho['restaurante_id'])
    taxa_entrega = float(restaurante['taxa_entrega']) if restaurante else 0.0

    itens_formatados = []
    subtotal = 0.0
    for item in carrinho['itens'].values():
        subtotal += item['preco'] * item['quantidade']
        itens_formatados.append((item['id'], item['quantidade'], item['preco']))

    total = subtotal + taxa_entrega

    pedido_id = PedidoModel.criar_pedido(
        usuario_id=session['user']['id'],
        restaurante_id=carrinho['restaurante_id'],
        endereco_entrega=endereco,
        total=total,
        itens=itens_formatados
    )

    session.pop('carrinho', None)
    flash('Pedido realizado com sucesso!', 'success')
    return redirect(url_for('pedidos.detalhes', id=pedido_id))

@pedidos_bp.route('/meus-pedidos')
def meus_pedidos():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    pedidos = PedidoModel.listar_por_usuario(session['user']['id'])
    return render_template('pedidos/meus_pedidos.html', pedidos=pedidos)

@pedidos_bp.route('/pedido/<int:id>')
def detalhes(id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    dados = PedidoModel.buscar_por_id(id)
    if not dados:
        flash('Pedido não encontrado.', 'danger')
        return redirect(url_for('pedidos.meus_pedidos'))

    return render_template('pedidos/detalhes.html', pedido=dados['pedido'], itens=dados['itens'])