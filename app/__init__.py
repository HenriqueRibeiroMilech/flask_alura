# Cria a aplicação Flask e conecta suas rotas.
from flask import Flask
from .routes.main import main_bp

def create_app():  # Factory: cria e devolve uma aplicação configurada.
    app = Flask(__name__)  # Usa este módulo como referência para localizar recursos.
    app.register_blueprint(main_bp)  # Adiciona as rotas do blueprint à aplicação.
    return app
