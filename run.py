# Inicia o servidor de desenvolvimento da aplicação.
from app import create_app

app = create_app()  # Cria a aplicação usando o factory.

if __name__ == '__main__':  # Executa o servidor apenas ao rodar este arquivo diretamente.
    app.run(debug=True)  # Ativa recarga automática e depuração durante o desenvolvimento.
