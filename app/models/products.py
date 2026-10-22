# Os modelos separam a estrutura dos dados da lógica de negócio.
from pydantic import BaseModel, Field, ConfigDict  # Field configura campos; ConfigDict define opções do modelo.
from typing import Optional
from bson import ObjectId

# BaseModel usa os tipos como um contrato: ao criar o objeto, valida os dados e gera erro se forem inválidos.
class Product(BaseModel):
    id: Optional[ObjectId] = Field(None, alias='_id')  # Liga o atributo id ao campo _id do MongoDB; pode ser omitido ou None.
    name: str  # A tipagem define o tipo esperado; name, price e stock são obrigatórios.
    price: float
    description: Optional[str] = None  # Aceita texto ou None; se não for enviada, assume None.
    stock: int

    model_config = ConfigDict(
        populate_by_name = True,  # Aceita também id na entrada, além do alias _id.
        arbitrary_types_allowed=True  # Permite usar ObjectId como tipo; não converte automaticamente strings em ObjectId.
    )

# Reutiliza os campos e a validação de Product e adapta a saída para as respostas da API.
class ProductDBModel(Product):
    def model_dump(self, *, mode='python', include=None, exclude=None, context=None, by_alias=None, exclude_unset=False, exclude_defaults=False, exclude_none=False, round_trip=False):
        # super() chama a serialização herdada do Pydantic, mantendo as opções recebidas.
        data = super().model_dump(mode=mode, include=include, exclude=exclude, context=context, by_alias=by_alias, exclude_unset=exclude_unset, exclude_defaults=exclude_defaults, exclude_none=exclude_none, round_trip=round_trip)
        if self.id:
            # Converte ObjectId em texto para o jsonify; esta implementação exige _id presente na saída.
            # As rotas garantem isso com by_alias=True e sem excluir o campo id.
            data["_id"] = str(data["_id"])
        return data  # Retorna um dicionário Python; a conversão para JSON será feita pelo Flask.
