from pydantic import BaseModel
from datetime import date  # Representa uma data, sem horário.

class Sale(BaseModel):  # Define os campos esperados para uma venda.
    sale_date: date  # O Pydantic também aceita e converte datas em texto no formato AAAA-MM-DD.
    product_id: str
    quantity: int
    total_value: float
