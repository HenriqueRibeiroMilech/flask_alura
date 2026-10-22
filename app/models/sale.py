from pydantic import BaseModel, ConfigDict
from datetime import date

# Os valores do CSV chegam como texto; o Pydantic valida e converte conforme os tipos declarados.
class Sale(BaseModel):
    sale_date: date  # Também podemos usar tipos como date para representar uma data sem horário.
    product_id: str
    quantity: int
    total_value: float

    model_config = ConfigDict(
        populate_by_name = True,  # Permite preencher pelos nomes dos campos; este modelo não define aliases.
        arbitrary_types_allowed=True  # Mantém a configuração usada na aula; não altera a serialização de datas.
    )
