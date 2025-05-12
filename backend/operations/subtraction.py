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
    raw_matrix_a = data.matrix_a
    raw_matrix_b = data.matrix_b

    error_validacion_dim = validar_dimensiones_para_suma_resta(raw_matrix_a, raw_matrix_b)
    if error_validacion_dim:
        return ApiResponse(success=False, error=error_validacion_dim)
    
    num_filas = len(raw_matrix_a)
    num_columnas = len(raw_matrix_a[0]) if num_filas > 0 else 0
    
    try:
        frac_matrix_a = [[to_fraction(el) for el in row] for row in raw_matrix_a]
        frac_matrix_b = [[to_fraction(el) for el in row] for row in raw_matrix_b]
    except ValueError as e:
        return ApiResponse(success=False, error=str(e))
    
    resultado_frac = [[Fraction(0) for _ in range(num_columnas)] for _ in range(num_filas)]
    pasos = ["Inicio de la resta de matrices A - B."]
    
    output_matrix_a_for_steps = [[format_fraction_output(el) for el in row] for row in frac_matrix_a]
    pasos.extend(format_matrix_for_steps(output_matrix_a_for_steps, "Matriz A"))
    output_matrix_b_for_steps = [[format_fraction_output(el) for el in row] for row in frac_matrix_b]
    pasos.extend(format_matrix_for_steps(output_matrix_b_for_steps, "Matriz B"))
    
    pasos.append("Calculando cada elemento de la matriz resultante C = A - B:")
    if num_columnas > 0: 
        for i in range(num_filas):
            for j in range(num_columnas):
                a_ij = frac_matrix_a[i][j]
                b_ij = frac_matrix_b[i][j]
                resta_elemento_frac = a_ij - b_ij
                resultado_frac[i][j] = resta_elemento_frac
                str_a_ij = format_fraction_output(a_ij)
                str_b_ij = format_fraction_output(b_ij)
                str_resta = format_fraction_output(resta_elemento_frac)
                pasos.append(f"  C({i+1},{j+1}) = A({i+1},{j+1}) - B({i+1},{j+1}) = {str_a_ij} - {str_b_ij} = {str_resta}")
                
    resultado_output = [[format_fraction_output(el) for el in row] for row in resultado_frac]
    pasos.append("Resta completada.")
    return ApiResponse(success=True, result=resultado_output, steps=pasos) 