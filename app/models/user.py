from pydantic import BaseModel

# Modelo específico dos dados enviados no login, sem representar um usuário completo.
class LoginPayload(BaseModel):
    username: str
    password: str
