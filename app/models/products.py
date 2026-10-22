# Os modelos separam a estrutura dos dados da lógica de negócio.
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId

# BaseModel usa os tipos como um contrato: ao criar o objeto, valida os dados e gera erro se forem inválidos.
class Product(BaseModel):
    id: Optional[ObjectId] = Field(None, alias='_id')
    name: str  # A tipagem define o tipo esperado; name, price e stock são obrigatórios.
    price: float
    description: Optional[str] = None  # Aceita texto ou None; se não for enviada, assume None.
    stock: int

    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed=True
    )

class ProductDBModel(Product):
    def model_dump(self, *, mode='python', include=None, exclude=None, context=None, by_alias=None, exclude_unset=False, exclude_defaults=False, exclude_none=False, round_trip=False):
        data = super().model_dump(mode=mode, include=include, exclude=exclude, context=context, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, round_trip=round_trip)
        if self.id:
            data["_id"] = str(data["_id"])
        return data