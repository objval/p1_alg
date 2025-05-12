from pydantic import BaseModel, Field, field_validator
from typing import List, Union, Any, Dict
from fractions import Fraction

# Definición para un elemento de matriz que puede ser int, float, o str (para fracciones)
MatrixElement = Union[int, float, str]

# Definición para una Matriz (lista de listas de MatrixElement)
InputMatrix = List[List[MatrixElement]] # Para la entrada que puede tener strings
Matrix = List[List[Fraction]]         # Para uso interno con Fracciones
OutputMatrix = List[List[str]]        # Para la salida, con fracciones como strings
OutputVector = List[str]              # Para la salida de un vector solución, con fracciones como strings

# Modelo Pydantic para la entrada de una matriz
class MatrixInput(BaseModel):
    matrix: InputMatrix

# Modelo Pydantic para la entrada de dos matrices
class TwoMatrixInput(BaseModel):
    matrix_a: InputMatrix
    matrix_b: InputMatrix

# Modelo Pydantic para la entrada de un sistema de ecuaciones Ax=b
class SystemInput(BaseModel):
    matrix_a: InputMatrix  # Coeficientes de la matriz A
    vector_b: List[MatrixElement]  # Vector de constantes b

# Nuevo modelo para el resultado de la Factorización LU
class LUFactorizationResult(BaseModel):
    matrix_l: OutputMatrix = Field(..., description="Matriz triangular inferior L")
    matrix_u: OutputMatrix = Field(..., description="Matriz triangular superior U")
    # Podríamos añadir una matriz de permutación P si implementamos LUP

# Modelo Pydantic para la respuesta estándar de la API
class ApiResponse(BaseModel):
    success: bool
    result: Union[OutputMatrix, str, LUFactorizationResult, Dict[str, Any], None] = Field(None, description="Resultado de la operación. Puede ser una matriz, un escalar (string), un objeto con L y U, un objeto de solución de sistema, o nulo.")
    steps: Union[List[str], None] = Field(None, description="Pasos detallados del cálculo.")
    error: Union[str, None] = Field(None, description="Mensaje de error si success es false.")

    @field_validator('result', mode='before')
    def set_result_none_if_not_success(cls, v, values):
        if not values.data.get('success') and v is None and values.data.get('error') is not None:
            return None
        return v 