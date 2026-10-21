from pydantic import BaseModel
from datetime import date

class Sale(BaseModel):
    sale_date: date  # Também podemos usar tipos como date para representar uma data sem horário.
    product_id: str
    quantity: int
    total_value: float
