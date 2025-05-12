from fastapi import APIRouter
from fractions import Fraction

from backend.models import TwoMatrixInput, ApiResponse
from backend.utils.validators import validar_dimensiones_para_suma_resta
from backend.utils.type_converters import to_fraction, format_fraction_output
from backend.utils.formatters import format_matrix_for_steps

router = APIRouter()

@router.post("/subtract", response_model=ApiResponse, summary="Resta de dos matrices")
async def subtract_matrices(data: TwoMatrixInput):
    """
    Resta dos matrices A y B (A - B). Los elementos pueden ser números o fracciones (ej. "1/2", "1 / 2").
    Valida la compatibilidad de dimensiones (hasta 4x4) y la validez de los elementos.
    Retorna la matriz resultante con elementos como enteros o strings de fracción.
    Incluye pasos del proceso en la respuesta, con formato mejorado para matrices.
    """
    raw_matrix_a = data.matrix_a # Obtener la matriz A sin procesar
    raw_matrix_b = data.matrix_b # Obtener la matriz B sin procesar

    error_validacion_dim = validar_dimensiones_para_suma_resta(raw_matrix_a, raw_matrix_b) # Validar las dimensiones de las matrices
    if error_validacion_dim:
        return ApiResponse(success=False, error=error_validacion_dim) # Retornar un error si las dimensiones no son válidas
    
    num_filas = len(raw_matrix_a) # Obtener el número de filas de la matriz A
    num_columnas = len(raw_matrix_a[0]) if num_filas > 0 else 0 # Obtener el número de columnas de la matriz A
    
    try:
        frac_matrix_a = [[to_fraction(el) for el in row] for row in raw_matrix_a] # Convertir la matriz A a fracciones
        frac_matrix_b = [[to_fraction(el) for el in row] for row in raw_matrix_b] # Convertir la matriz B a fracciones
    except ValueError as e:
        return ApiResponse(success=False, error=str(e)) # Retornar un error si la conversión a fracción falla
    
    resultado_frac = [[Fraction(0) for _ in range(num_columnas)] for _ in range(num_filas)] # Inicializar la matriz resultante con ceros
    pasos = ["Inicio de la resta de matrices A - B."] # Inicializar los pasos con un mensaje de inicio
    
    output_matrix_a_for_steps = [[format_fraction_output(el) for el in row] for row in frac_matrix_a] # Formatear la matriz A para los pasos
    pasos.extend(format_matrix_for_steps(output_matrix_a_for_steps, "Matriz A")) # Agregar la matriz A formateada a los pasos
    output_matrix_b_for_steps = [[format_fraction_output(el) for el in row] for row in frac_matrix_b] # Formatear la matriz B para los pasos
    pasos.extend(format_matrix_for_steps(output_matrix_b_for_steps, "Matriz B")) # Agregar la matriz B formateada a los pasos
    
    pasos.append("Calculando cada elemento de la matriz resultante C = A - B:") # Agregar un paso para indicar el cálculo de la matriz resultante
    if num_columnas > 0: 
        for i in range(num_filas): # Iterar sobre las filas
            for j in range(num_columnas): # Iterar sobre las columnas
                a_ij = frac_matrix_a[i][j] # Obtener el elemento A[i][j]
                b_ij = frac_matrix_b[i][j] # Obtener el elemento B[i][j]
                resta_elemento_frac = a_ij - b_ij # Calcular la resta del elemento
                resultado_frac[i][j] = resta_elemento_frac # Asignar el resultado a la matriz resultante
                str_a_ij = format_fraction_output(a_ij) # Formatear el elemento A[i][j] para mostrarlo en los pasos
                str_b_ij = format_fraction_output(b_ij) # Formatear el elemento B[i][j] para mostrarlo en los pasos
                str_resta = format_fraction_output(resta_elemento_frac) # Formatear el resultado de la resta para mostrarlo en los pasos
                pasos.append(f"  C({i+1},{j+1}) = A({i+1},{j+1}) - B({i+1},{j+1}) = {str_a_ij} - {str_b_ij} = {str_resta}") # Agregar el paso del cálculo al registro
                
    resultado_output = [[format_fraction_output(el) for el in row] for row in resultado_frac] # Formatear la matriz resultante para la salida
    pasos.append("Resta completada.") # Agregar un paso para indicar que la resta se ha completado
    return ApiResponse(success=True, result=resultado_output, steps=pasos) # Retornar la respuesta de la API con la matriz resultante y los pasos