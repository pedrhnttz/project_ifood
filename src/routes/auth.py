from flask import Blueprint, redirect, url_for, session, render_template, request, flash
from authlib.integrations.flask_client import OAuth
from src.models.usuario import UsuarioModel
from src.config import Config

auth_bp = Blueprint('auth', __name__)

oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

@auth_bp.route('/login')
def login():
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/callback')
def google_callback():
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')
    
    if user_info:
        usuario = UsuarioModel.criar_ou_atualizar(
            nome=user_info.get('name'),
            email=user_info.get('email'),
            google_id=user_info.get('sub')
        )
        
        session['user'] = {
            'id': usuario['id'],
            'nome': usuario['nome'],
            'email': usuario['email']
        }
        flash('Login efetuado com sucesso!', 'success')
    
    return redirect(url_for('restaurantes.listar'))

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Sessão encerrada com sucesso.', 'info')
    return redirect(url_for('restaurantes.listar'))