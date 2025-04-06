from pydantic import BaseModel, EmailStr, validator
from typing import List

class InputSchema(BaseModel):
    """Schema para validar os dados de entrada."""
    valor_emprestimo: float
    taxa_juros: float
    prazo: int
    carencia: int = 0  # Valor padrão para carência

    @validator("valor_emprestimo", "taxa_juros", "prazo")
    def validar_positivos(cls, valor):
        if valor <= 0:
            raise ValueError("Os valores devem ser positivos.")
        return valor

    @validator("carencia")
    def validar_carencia(cls, carencia):
        if carencia < 0:
            raise ValueError("A carência não pode ser negativa.")
        return carencia


class OutputSchema(BaseModel):
    """Schema para representar os dados de saída."""
    prestacoes: List[float]
    saldos_devedores: List[float]
    iof: float
    valor_liquido: float
