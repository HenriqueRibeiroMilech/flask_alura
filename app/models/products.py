# Os modelos separam a estrutura dos dados da lógica de negócio.
from pydantic import BaseModel
from typing import Optional

# BaseModel usa os tipos como um contrato: ao criar o objeto, valida os dados e gera erro se forem inválidos.
class Product(BaseModel):
    name: str  # A tipagem define o tipo esperado; name, price e stock são obrigatórios.
    price: float
    description: Optional[str] = None  # Aceita texto ou None; se não for enviada, assume None.
    stock: int
