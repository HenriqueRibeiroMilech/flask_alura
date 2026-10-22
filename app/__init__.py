# Cria a aplicação Flask e conecta suas rotas.
from flask import Flask
from pymongo import MongoClient  # Cliente usado para acessar o MongoDB pelo Python.

db = None  # Referência ao banco, preenchida pela factory antes da importação das rotas.

def create_app():  # Factory: cria e devolve uma aplicação configurada.
    app = Flask(__name__)  # Usa este módulo como referência para localizar recursos.
    app.config.from_object('config.Config')  # Carrega os atributos em maiúsculas da classe Config.
    global db  # Permite atribuir à variável do módulo, em vez de criar uma variável local.

    try:
        # Criar o cliente não garante que o servidor esteja acessível; as consultas podem falhar depois.
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()  # Seleciona o banco indicado no caminho da MONGO_URI.
    except Exception as e:
        # Registra a falha de configuração/inicialização; a aplicação continua mesmo sem o banco.
        print(f'Erro ao realizar a conexao com o banco de dados: {e}')

    # Importa após definir db: as rotas também importam app, evitando uma importação circular prematura.
    from .routes.main import main_bp
    app.register_blueprint(main_bp)  # Adiciona as rotas do blueprint à aplicação.

    return app
