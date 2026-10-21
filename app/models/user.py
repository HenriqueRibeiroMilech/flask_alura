from pydantic import BaseModel

class Login(BaseModel):  # Define os dados de entrada do login; a autenticação será feita separadamente.
    username: str
    password: str
