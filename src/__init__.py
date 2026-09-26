import os
from flask import Flask
from src.config import Config
from src.db import init_app as init_db_app
from src.routes import auth_bp, init_oauth, usuarios_bp, restaurantes_bp, refeicoes_bp, pedidos_bp

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(Config)

    init_db_app(app)
    init_oauth(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(restaurantes_bp, url_prefix='/restaurantes')
    app.register_blueprint(refeicoes_bp, url_prefix='/refeicoes')
    app.register_blueprint(pedidos_bp, url_prefix='/pedidos')

    @app.route('/')
    def index():
        return "Aplicação iniciada com sucesso! Acesse <a href='/restaurantes/'>/restaurantes/</a>"

    return app