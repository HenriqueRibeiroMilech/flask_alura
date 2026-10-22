# Define as rotas principais da API e suas respostas em JSON.
from flask import Blueprint, jsonify, request, current_app  # request permite acessar os dados enviados na requisição.
from app.models.user import LoginPayload  # Define os campos e tipos esperados no corpo do login.
from pydantic import ValidationError  # Exceção gerada quando os dados não atendem ao modelo.
from app import db  # Banco selecionado na factory; db.products acessa a coleção products.
from bson import ObjectId  # Tipo BSON usado pelo MongoDB para o _id padrão dos documentos.
from app.models.products import *
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt

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
        token = jwt.encode(
            {
                "user_id": user_data.username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            }, 
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        return jsonify({'access_token': token}), 200
    # Sem status explícito, esta resposta também retorna HTTP 200 por padrão.
    return jsonify({"message":"Credenciais invalidas!"})

# RF: O sistema deve permitir a listagem de todos os produtos.
@main_bp.route('/products', methods=['GET'])  # GET consulta ou obtem informações de recursos.
def get_products():
    products_cursor = db.products.find({})  # Filtro vazio busca todos os documentos, como find().
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]

    return jsonify(products_list)

# RF: O sistema deve permitir a criação de um novo produto.
@token_required
@main_bp.route('/products', methods=['POST'])
def create_product(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()})

    result = db.products.insert_one(product.model_dump())
    
    return jsonify({"message":"Rota de criação de produtos",
                    "id": str(result.inserted_id)}), 201

# RF: O sistema deve permitir a visualização de um unico produto existente.
@main_bp.route('/product/<string:product_id>', methods=['GET'])  # Recebe o ID como texto, pois pode conter letras e números.
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)  # Converte o texto da URL para o tipo armazenado no campo _id.
    except Exception as e:
        # Trata a conversão de IDs inválidos; sem status explícito, a resposta usa HTTP 200.
        return jsonify({"error":f"Erro ao transformar o {product_id} em ObjectId: {e}"})

    product = db.products.find_one({'_id':oid})  # Retorna um documento ou None; falhas de consulta não entram no try acima.

    if product:
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model)
    else:
        # Mantém o comportamento da aula: produto ausente também retorna HTTP 200.
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
