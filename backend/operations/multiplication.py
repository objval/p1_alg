from fastapi import APIRouter, HTTPException
from typing import List
from fractions import Fraction

from backend.models import TwoMatrixInput, ApiResponse, Matrix
from backend.utils.type_converters import to_fraction, format_fraction_output
from backend.utils.formatters import format_matrix_for_steps
from backend.utils.validators import validar_matriz, validar_dimensiones_para_multiplicacion

router = APIRouter()

@router.post("/multiply", response_model=ApiResponse, summary="Multiplicación de dos matrices")
def multiply_matrices_endpoint(data: TwoMatrixInput):
    """
    Multiplica dos matrices A y B.

    La multiplicación de matrices A (de dimensiones m x n) y B (de dimensiones n x p)
    resulta en una matriz C (de dimensiones m x p) donde cada elemento C[i][j]
    es el producto punto de la fila i de A y la columna j de B.
    C[i][j] = A[i][0]*B[0][j] + A[i][1]*B[1][j] + ... + A[i][n-1]*B[n-1][j]
    """
    steps = []
    error_msg = None

    # Validar y convertir Matriz A
    rows_a, cols_a, error_msg_a = validar_matriz(data.matrix_a, "A")
    if error_msg_a:
        raise HTTPException(status_code=400, detail=error_msg_a)
    
    matrix_a_frac: Matrix = []
    try:
        for i, row_a in enumerate(data.matrix_a):
            row_a_frac = []
            for j, val_a in enumerate(row_a):
                row_a_frac.append(to_fraction(val_a))
            matrix_a_frac.append(row_a_frac)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    steps.append("Matriz A ingresada:")
    steps.extend(format_matrix_for_steps(matrix_a_frac, "Matriz A"))

    # Validar y convertir Matriz B
    rows_b_val, cols_b_val, error_msg_b = validar_matriz(data.matrix_b, "B")
    if error_msg_b:
        raise HTTPException(status_code=400, detail=error_msg_b)

    # Verificar límites de tamaño antes de continuar
    if rows_a is not None and rows_a > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 filas. La matriz A tiene {rows_a} filas.")
    if cols_a is not None and cols_a > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 columnas. La matriz A tiene {cols_a} columnas.")
    if rows_b_val is not None and rows_b_val > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 filas. La matriz B tiene {rows_b_val} filas.")
    if cols_b_val is not None and cols_b_val > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 columnas. La matriz B tiene {cols_b_val} columnas.")

    matrix_b_frac: Matrix = []
    try:
        for i, row_b in enumerate(data.matrix_b):
            row_b_frac = []
            for j, val_b in enumerate(row_b):
                row_b_frac.append(to_fraction(val_b))
            matrix_b_frac.append(row_b_frac)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    steps.append("Matriz B ingresada:")
    steps.extend(format_matrix_for_steps(matrix_b_frac, "Matriz B"))

    # Validar dimensiones para multiplicación
    valid_dims, dim_error_msg = validar_dimensiones_para_multiplicacion(matrix_a_frac, matrix_b_frac)
    if not valid_dims:
        raise HTTPException(status_code=400, detail=dim_error_msg)

    # Lógica de multiplicación
    rows_a = len(matrix_a_frac)
    cols_a = len(matrix_a_frac[0]) # También es rows_b
    cols_b = len(matrix_b_frac[0])

    result_matrix_frac: Matrix = [[Fraction(0) for _ in range(cols_b)] for _ in range(rows_a)]
    calculation_steps = []

    steps.append("Proceso de multiplicación (A x B):")
    for i in range(rows_a):
        for j in range(cols_b):
            dot_product = Fraction(0)
            step_detail = f"Elemento C[{i+1}][{j+1}] = "
            calculation_parts = []
            for k in range(cols_a): # cols_a es igual a rows_b
                term = matrix_a_frac[i][k] * matrix_b_frac[k][j]
                dot_product += term
                calculation_parts.append(f"({format_fraction_output(matrix_a_frac[i][k])} * {format_fraction_output(matrix_b_frac[k][j])})")
            step_detail += " + ".join(calculation_parts)
            step_detail += f" = {format_fraction_output(dot_product)}"
            calculation_steps.append(step_detail)
            result_matrix_frac[i][j] = dot_product
    
    steps.extend(calculation_steps)
    steps.append("Matriz Resultante (C = A x B):")
    steps.extend(format_matrix_for_steps(result_matrix_frac, "Matriz Resultante C"))

    # Formatear resultado para la API
    result_matrix_formatted = [
        [format_fraction_output(val) for val in row]
        for row in result_matrix_frac
    ]

    return ApiResponse(
        success=True,
        result=result_matrix_formatted,
        steps=steps
    ) 