from functools import wraps  # Preserva nome e metadados da função original para o Flask.
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # Espera o cabeçalho Authorization no formato Bearer <token>.
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'message': 'Token Malformado'}), 401
        if not token:
            return jsonify({'error':'Token não encontrado'}), 401

        # Confere a assinatura e a expiração; aceita somente o algoritmo HS256.
        try:
            data = jwt.decode(token,
                              current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error':'Token Expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error':'Token Inválido'}), 401

        # Só executa a rota após validar o token e repassa os dados do usuário.
        return f(data, *args, **kwargs)

    return decorated
