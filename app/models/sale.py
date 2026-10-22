from pydantic import BaseModel, ConfigDict
from datetime import date

class Sale(BaseModel):
    sale_date: date  # Também podemos usar tipos como date para representar uma data sem horário.
    product_id: str
    quantity: int
    total_value: float

    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed=True 
    )