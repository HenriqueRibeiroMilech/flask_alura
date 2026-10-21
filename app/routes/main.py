# Define as rotas principais da API e suas respostas em JSON.
from flask import Blueprint, jsonify

main_bp = Blueprint('main_bp', __name__)  # Agrupa as rotas para registro na aplicação.

@main_bp.route('/')  # Associa a URL raiz à função abaixo; GET por padrão.
def index():
    return jsonify({"message":"Rota inical do app"})  # Converte o dicionário em resposta JSON.

@main_bp.route('/products')  # Rota de produtos; GET por padrão.
def get_products():
    return jsonify({"message":"Rota de listagem de produtos"})

@main_bp.route('/login', methods=['POST'])  # Aceita POST; acessar pelo navegador com GET retorna 405.
def login():  # Por enquanto, só retorna uma mensagem, sem autenticar usuários.
    return jsonify({"message":"Rota de listagem de produtos"})
