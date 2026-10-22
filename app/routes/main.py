# Define as rotas principais da API e suas respostas em JSON.
from flask import Blueprint, jsonify, request, current_app  # request permite acessar os dados enviados na requisição.
from app.models.user import LoginPayload  # Define os campos e tipos esperados no corpo do login.
from pydantic import ValidationError  # Exceção gerada quando os dados não atendem ao modelo.
from app import db  # Banco selecionado na factory; db.products acessa a coleção products.
from bson import ObjectId  # Tipo BSON usado pelo MongoDB para o _id padrão dos documentos.
from app.models.products import *  # Disponibiliza os modelos usados na validação e nas respostas.
from app.decorators import token_required  # Exige um JWT válido antes de executar a rota protegida.
from datetime import datetime, timedelta, timezone  # Calcula a expiração usando horário UTC.
import jwt  # PyJWT assina e valida tokens; o conteúdo do token não é criptografado.
import csv  # Biblioteca padrão para ler os registros do arquivo CSV.
import os
import io  # Permite tratar o texto recebido como um arquivo em memória.
from app.models.sale import Sale  # Valida e converte os campos de cada venda.

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

    # Valida credenciais fixas para emitir o token; ainda não consulta usuários no banco.
    # Os campos são strings, por isso a senha também é comparada com um texto.
    if user_data.username == 'admin' and user_data.password == '123':
        # Assina a identificação do usuário e a expiração de 30 minutos com a chave da aplicação.
        token = jwt.encode(
            {
                "user_id": user_data.username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            }, 
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        return jsonify({'access_token': token}), 200
    return jsonify({"error":"Credenciais inválidas"}), 401

# RF: O sistema deve permitir a listagem de todos os produtos.
@main_bp.route('/products', methods=['GET'])  # GET consulta ou obtem informações de recursos.
def get_products():
    products_cursor = db.products.find({})  # Filtro vazio busca todos os documentos, como find().
    # A compreensão de lista percorre o cursor; **product passa os campos de cada documento ao modelo para validação.
    # by_alias=True usa _id na saída; exclude_none=True omite apenas valores None, preservando zero e texto vazio.
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]

    return jsonify(products_list)

# RF: O sistema deve permitir a criação de um novo produto.
@main_bp.route('/products', methods=['POST'])
@token_required  # Aplicado primeiro para que o Flask registre a função já protegida.
def create_product(token):  # Recebe os dados decodificados do JWT, repassados pelo decorator.
    try:
        product = Product(**request.get_json())  # Valida os campos do corpo JSON antes da inserção.
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    # Converte o modelo validado em um dicionário para inserir o documento, conforme a aula.
    result = db.products.insert_one(product.model_dump())
    
    return jsonify({"message":"Produto criado com sucesso",
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
        # Aplica a mesma validação e serialização da listagem, agora a um único documento.
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model)
    else:
        # Mantém o comportamento da aula: produto ausente também retorna HTTP 200.
        return jsonify({"error":f"Produto com o id: {product_id} - Não encontrado"})

# RF: O sistema deve permitir a atualização de um unico produto existente.
@main_bp.route('/product/<string:product_id>', methods=['PUT'])  # Recebe o ID do MongoDB como texto, conforme a aula.
@token_required  # Exige autenticação antes de executar a atualização.
def update_product(token, product_id):  # O decorator repassa os dados do JWT como primeiro argumento.
    try:
        oid = ObjectId(product_id)  # Converte o ID da URL para o tipo usado no banco.
        update_data = UpdateProduct(**request.get_json())  # Valida somente os dados enviados para alteração.
        update_result = db.products.update_one(
            {"_id": oid},
            # $set altera os campos indicados, preservando os demais campos do documento.
            # exclude_unset=True omite campos não enviados; um None explícito continua incluído.
            {"$set": update_data.model_dump(exclude_unset=True)}
        )
        # matched_count verifica se o produto existe, mesmo quando os valores enviados são iguais aos atuais.
        if update_result.matched_count == 0:
            return jsonify({"error": "Produto não encontrado"}), 404
        updated_product = db.products.find_one({"_id": oid})  # Consulta novamente para retornar o documento atualizado.
        # Valida o documento e converte seu _id em texto antes de gerar a resposta JSON.
        return jsonify(ProductDBModel(**updated_product).model_dump(by_alias=True, exclude_none=True))
    except ValidationError as e:
        # Mantém a resposta da aula, sem status explícito (HTTP 200); não captura erros de ObjectId.
        return jsonify({"error": e.errors()})

# RF: O sistema deve permitir a deleção de um unico produto existente.
@main_bp.route('/product/<string:product_id>', methods=['DELETE'])  # Recebe o ID como texto para convertê-lo em ObjectId.
@token_required  # Somente requisições autenticadas podem excluir produtos.
def delete_product(token, product_id):
    try:
        oid = ObjectId(product_id)
        delete_product = db.products.delete_one({"_id": oid})  # Exclui um único documento com esse ID.
        # O resultado informa quantos documentos foram excluídos; zero indica produto ausente.
        if delete_product.deleted_count == 0:
            return jsonify({"error": "Produto não foi encontrado"}), 404
        return "", 204  # HTTP 204 indica sucesso sem corpo de resposta.
    except Exception:
        # Como na aula, qualquer exceção neste bloco recebe a mesma mensagem e o status 400.
        return jsonify({"error": "id do produto inválido"}), 400

# RF: O sistema deve permitir a importação de vendas através de um arquivo.
@main_bp.route('/sales/upload', methods=['POST'])
@token_required  # Restringe o upload a requisições com JWT válido.
def upload_sales(token):
    # O cliente deve enviar o arquivo via form-data, usando a chave file.
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo foi enviado"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    # Confere a extensão do nome, conforme a aula; isso não valida o conteúdo do arquivo.
    if file and file.filename.endswith('.csv'):
        # Lê os bytes, decodifica em UTF-8 e cria um arquivo de texto em memória.
        csv_stream = io.StringIO(file.stream.read().decode('UTF-8'), newline=None)
        csv_reader = csv.DictReader(csv_stream)  # Usa o cabeçalho como chaves de cada linha.

        sales_to_insert = []  # Acumula as vendas que passaram pela validação.
        errors = []  # Guarda os erros sem interromper o processamento das demais linhas.

        # Numera os registros a partir de 1; o cabeçalho já foi consumido pelo DictReader.
        for row_num, row in enumerate(csv_reader, 1):
            try:
                sale_data = Sale(**row)  # Distribui as colunas nos campos do modelo para validação e conversão.
                sales_to_insert.append(sale_data.model_dump())  # Prepara um dicionário para a inserção.
            except ValidationError as e:
                errors.append(f"Linha {row_num}: Dados inválidos - {e.errors()}")
            except Exception as e:
                errors.append(f"Linha {row_num}: Erro inesperado ao processar a linha - {str(e)}")

        # Fora do for: insere o lote uma única vez, após validar todos os registros.
        if sales_to_insert:
            try:
                db.sales.insert_many(sales_to_insert)
            except Exception as e:
                return jsonify({"error": f"Erro ao inserir dados no banco: {str(e)}"}), 500

        # Retorna a quantidade de vendas válidas e os erros coletados, inclusive quando nenhuma é válida.
        return jsonify({
            "message": "Upload processado com sucesso.",
            "vendas_importadas": len(sales_to_insert),
            "erros_encontrados": errors
        }), 200
