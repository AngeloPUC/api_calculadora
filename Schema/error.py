from pydantic import BaseModel

class InvalidInputError(Exception):
    """Erro personalizado para entradas inválidas no cálculo."""
    def __init__(self, message="Entrada inválida fornecida. Por favor, revise os parâmetros."):
        self.message = message
        super().__init__(self.message)
