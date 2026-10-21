from pydantic import BaseModel  # Base para modelos que validam os dados conforme os tipos declarados.
from typing import Optional

class Product(BaseModel):  # Define os campos esperados para um produto.
    name: str  # Campos sem valor padrão são obrigatórios ao criar o modelo.
    price: float
    description: Optional[str] = None  # Aceita texto ou None; pode ser omitida por ter valor padrão.
    stock: int
