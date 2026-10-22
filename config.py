import os  # Permite consultar as variáveis de ambiente do processo.
from dotenv import load_dotenv  # Carrega as configurações locais definidas no arquivo .env.

load_dotenv()  # Deve executar antes de os.getenv para disponibilizar os valores do .env.

# Centraliza as configurações que a factory carregará na aplicação Flask.
class Config:
    MONGO_URI = os.getenv('MONGO_URI')  # A URI inclui o servidor e o nome do banco que será utilizado.
    SECRET_KEY = os.getenv('SECRET_KEY')