from pydantic import BaseModel

# Modelo específico dos dados enviados no login, sem representar um usuário completo.
class Login(BaseModel):
    username: str
    password: str
