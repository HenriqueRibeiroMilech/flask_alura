# Cria a aplicação Flask e conecta suas rotas.
from flask import Flask
from pymongo import MongoClient

db = None

def create_app():  # Factory: cria e devolve uma aplicação configurada.
    app = Flask(__name__)  # Usa este módulo como referência para localizar recursos.
    app.config.from_object('config.Config')
    global db

    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()
    except Exception as e:
        print(f'Erro ao realizar a conexao com o banco de dados: {e}')

    from .routes.main import main_bp
    app.register_blueprint(main_bp)  # Adiciona as rotas do blueprint à aplicação.

    return app
