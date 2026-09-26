from flask import Flask
from src.config import Config
from src.db import init_app as init_db_app
from src.routes import auth_bp, usuarios_bp, restaurantes_bp, refeicoes_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(restaurantes_bp, url_prefix='/restaurantes')
    app.register_blueprint(refeicoes_bp, url_prefix='/refeicoes')

    @app.route('/')
    def index():
        return "Aplicação iFood iniciada com sucesso! Acesse as rotas no navegador."

    return app