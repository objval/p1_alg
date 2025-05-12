from fastapi import APIRouter
from fractions import Fraction

from backend.models import TwoMatrixInput, ApiResponse
from backend.utils.validators import validar_dimensiones_para_suma_resta
from backend.utils.type_converters import to_fraction, format_fraction_output
from backend.utils.formatters import format_matrix_for_steps

router = APIRouter()

@router.post("/add", response_model=ApiResponse, summary="Suma de dos matrices")
async def add_matrices(data: TwoMatrixInput):
    """
    Suma dos matrices A y B. Los elementos pueden ser números o fracciones (ej. "1/2", "1 / 2").
    Valida la compatibilidad de dimensiones (hasta 4x4) y la validez de los elementos.
    Retorna la matriz resultante con elementos como enteros o strings de fracción.
    Incluye pasos del proceso en la respuesta, con formato mejorado para matrices.
    """
    raw_matrix_a = data.matrix_a  # Obtiene la matriz A sin procesar desde la entrada
    raw_matrix_b = data.matrix_b  # Obtiene la matriz B sin procesar desde la entrada
    error_validacion_dim = validar_dimensiones_para_suma_resta(raw_matrix_a, raw_matrix_b)  # Valida si las dimensiones de las matrices son compatibles para la suma
    if error_validacion_dim: return ApiResponse(success=False, error=error_validacion_dim)  # Si la validación falla, retorna un error en la respuesta
    
    num_filas = len(raw_matrix_a)  # Obtiene el número de filas de la matriz A
    num_columnas = len(raw_matrix_a[0]) if num_filas > 0 else 0  # Obtiene el número de columnas de la matriz A (si hay filas)
    
    try:
        frac_matrix_a = [[to_fraction(el) for el in row] for row in raw_matrix_a]  # Convierte los elementos de la matriz A a objetos Fraction
        frac_matrix_b = [[to_fraction(el) for el in row] for row in raw_matrix_b]  # Convierte los elementos de la matriz B a objetos Fraction
    except ValueError as e: return ApiResponse(success=False, error=str(e))  # Si la conversión falla, retorna un error en la respuesta
    
    resultado_frac = [[Fraction(0) for _ in range(num_columnas)] for _ in range(num_filas)]  # Inicializa la matriz resultante con elementos Fraction(0)
    pasos = ["Inicio de la suma de matrices A y B."]  # Inicializa la lista de pasos con un mensaje de inicio
    
    output_matrix_a_for_steps = [[format_fraction_output(el) for el in row] for row in frac_matrix_a]  # Formatea la matriz A para mostrar en los pasos
    pasos.extend(format_matrix_for_steps(output_matrix_a_for_steps, "Matriz A"))  # Agrega la matriz A formateada a la lista de pasos
    output_matrix_b_for_steps = [[format_fraction_output(el) for el in row] for row in frac_matrix_b]  # Formatea la matriz B para mostrar en los pasos
    pasos.extend(format_matrix_for_steps(output_matrix_b_for_steps, "Matriz B"))  # Agrega la matriz B formateada a la lista de pasos
    
    pasos.append("Calculando cada elemento de la matriz resultante C = A + B:")  # Agrega un mensaje a la lista de pasos
    if num_columnas > 0:  # Si hay columnas en las matrices
        for i in range(num_filas):  # Itera sobre las filas
            for j in range(num_columnas):  # Itera sobre las columnas
                a_ij = frac_matrix_a[i][j]  # Obtiene el elemento A(i,j) como Fraction
                b_ij = frac_matrix_b[i][j]  # Obtiene el elemento B(i,j) como Fraction
                suma_elemento_frac = a_ij + b_ij  # Suma los elementos A(i,j) y B(i,j)
                resultado_frac[i][j] = suma_elemento_frac  # Asigna la suma al elemento C(i,j) de la matriz resultante
                str_a_ij = format_fraction_output(a_ij)  # Formatea el elemento A(i,j) para mostrar en los pasos
                str_b_ij = format_fraction_output(b_ij)  # Formatea el elemento B(i,j) para mostrar en los pasos
                str_suma = format_fraction_output(suma_elemento_frac)  # Formatea la suma para mostrar en los pasos
                pasos.append(f"  C({i+1},{j+1}) = A({i+1},{j+1}) + B({i+1},{j+1}) = {str_a_ij} + {str_b_ij} = {str_suma}")  # Agrega el paso de suma a la lista de pasos
                
    resultado_output = [[format_fraction_output(el) for el in row] for row in resultado_frac]  # Formatea la matriz resultante para la salida
    pasos.append("Suma completada.")  # Agrega un mensaje de finalización a la lista de pasos
    return ApiResponse(success=True, result=resultado_output, steps=pasos)  # Retorna la respuesta exitosa con la matriz resultante y los pasos