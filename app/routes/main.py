# Define as rotas principais da API e suas respostas em JSON.
from flask import Blueprint, jsonify, request  # request permite acessar os dados enviados na requisição.
from app.models.user import LoginPayload  # Define os campos e tipos esperados no corpo do login.
from pydantic import ValidationError  # Exceção gerada quando os dados não atendem ao modelo.
from app import db
from bson import ObjectId

main_bp = Blueprint('main_bp', __name__)  # Agrupa as rotas para registro na aplicação.

@main_bp.route('/')  # Associa a URL raiz à função abaixo; GET por padrão.
def index():
    return jsonify({"message":"Rota inical do app"})  # Converte o dicionário em resposta JSON.

# RF = Requisitos Funcionais: descrevem o que o sistema deve permitir fazer.

# RF: O sistema deve permitir que um usuário se autentique para obter um token.
@main_bp.route('/login', methods=['POST'])  # POST envia dados de um recurso para o servidor.
def login():
    # O try permite tratar falhas na leitura e na validação dos dados recebidos.
    try:
        raw_data = request.get_json()  # Converte o corpo JSON em um objeto Python; esperamos um dicionário.
        user_data = LoginPayload(**raw_data)  # ** distribui as chaves como argumentos; o Pydantic valida os campos.
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400  # Retorna os detalhes da validação e o status de requisição inválida.
    except Exception as e:
        return jsonify({"error": "Erro durante a requisição do dado"}), 500  # Outras exceções recebem uma mensagem genérica.

    # Simula a autenticação com credenciais fixas; ainda não consulta usuários nem gera tokens.
    # Os campos são strings, por isso a senha também é comparada com um texto.
    if user_data.username == 'admin' and user_data.password == '123':
        return jsonify({"message":"Login bem-sucedido!"})
    else:
        # Sem status explícito, esta resposta também retorna HTTP 200 por padrão.
        return jsonify({"message":"Credenciais invalidas!"})

# RF: O sistema deve permitir a listagem de todos os produtos.
@main_bp.route('/products', methods=['GET'])  # GET consulta ou obtem informações de recursos.
def get_products():
    products_cursor = db.products.find({})
    products_list = []

    for products in products_cursor:
        products['_id'] = str(products['_id'])
        products_list.append(products)

    return jsonify(products_list)

# RF: O sistema deve permitir a criação de um novo produto.
@main_bp.route('/products', methods=['POST'])
def create_product():
    return jsonify({"message":"Rota de criação de produtos"})

# RF: O sistema deve permitir a visualização de um unico produto existente.
@main_bp.route('/product/<string:product_id>', methods=['GET'])  # Captura o ID da URL como inteiro e o passa à função.
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({"error":f"Erro ao transformar o {product_id} em ObjectId: {e}"})

    product = db.products.find_one({'_id':oid})

    if product:
        product['_id'] = str(product['_id'])
        return jsonify(product)
    else:
        return jsonify({"error":f"Produto com o id: {product_id} - Não encontrado"})

# RF: O sistema deve permitir a atualização de um unico produto existente.
@main_bp.route('/product/<int:product_id>', methods=['PUT'])  # PUT indica a atualização de um recurso.
def update_product(product_id):
    return jsonify({"message":f"Rota de atualização do produto {product_id}"})

# RF: O sistema deve permitir a deleção de um unico produto existente.
@main_bp.route('/product/<int:product_id>', methods=['DELETE'])  # DELETE indica a exclusão de um recurso.
def delete_product(product_id):
    return jsonify({"message":f"Rota de deleção do produto {product_id}"})

# RF: O sistema deve permitir a importação de vendas através de um arquivo.
@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({"message":"Rota de upload de arquivo de vendas"})
