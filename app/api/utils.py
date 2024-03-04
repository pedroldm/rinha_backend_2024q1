from typing import TypedDict

class TransactionPayload(TypedDict):
    valor: int
    tipo: str
    descricao: str

