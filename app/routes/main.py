# Define as rotas principais da API e suas respostas em JSON.
from flask import Blueprint, jsonify

main_bp = Blueprint('main_bp', __name__)  # Agrupa as rotas para registro na aplicação.

@main_bp.route('/')  # Associa a URL raiz à função abaixo; GET por padrão.
def index():
    return jsonify({"message":"Rota inical do app"})  # Converte o dicionário em resposta JSON.

# RF = Requisitos Funcionais.

# RF: O sistema deve permitir que um usuário se autentique para obter um token.
@main_bp.route('/login', methods=['POST'])  # Aceita POST; acessar pelo navegador com GET retorna 405.
def login():  # Por enquanto, só retorna uma mensagem, sem autenticar usuários.
    return jsonify({"message":"Realizar o login"})

# RF: O sistema deve permitir a listagem de todos os produtos.
@main_bp.route('/products', methods=['GET'])  # Rota de produtos.
def get_products():
    return jsonify({"message":"Rota de listagem de produtos"})

# RF: O sistema deve permitir a criação de um novo produto.
@main_bp.route('/products', methods=['POST'])
def create_product():
    return jsonify({"message":"Rota de criação de produtos"})

# RF: O sistema deve permitir a visualização de um unico produto existente.
@main_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    return jsonify({"message":f"Rota de visualização detalhada do produto {product_id}"})

# RF: O sistema deve permitir a atualização de um unico produto existente.
@main_bp.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return jsonify({"message":f"Rota de atualização do produto {product_id}"})

# RF: O sistema deve permitir a deleção de um unico produto existente.
@main_bp.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return jsonify({"message":f"Rota de deleção do produto {product_id}"})

# RF: O sistema deve permitir a importação de vendas através de um arquivo.
@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({"message":"Rota de upload de arquivo de vendas"})