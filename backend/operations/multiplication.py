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
    steps = [] # Lista para almacenar los pasos de la operación
    error_msg = None # Variable para almacenar mensajes de error

    # Validar y convertir Matriz A
    rows_a, cols_a, error_msg_a = validar_matriz(data.matrix_a, "A") # Validar la matriz A
    if error_msg_a:
        raise HTTPException(status_code=400, detail=error_msg_a) # Lanzar excepción si hay un error en la matriz A
    
    matrix_a_frac: Matrix = [] # Inicializar la matriz A como una lista de listas de fracciones
    try:
        for i, row_a in enumerate(data.matrix_a): # Iterar sobre las filas de la matriz A
            row_a_frac = [] # Inicializar la fila como una lista de fracciones
            for j, val_a in enumerate(row_a): # Iterar sobre los valores de la fila
                row_a_frac.append(to_fraction(val_a)) # Convertir el valor a fracción y agregarlo a la fila
            matrix_a_frac.append(row_a_frac) # Agregar la fila a la matriz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) # Lanzar excepción si hay un error de conversión

    steps.append("Matriz A ingresada:") # Agregar un paso al registro
    steps.extend(format_matrix_for_steps(matrix_a_frac, "Matriz A")) # Agregar la matriz A formateada a los pasos

    # Validar y convertir Matriz B
    rows_b_val, cols_b_val, error_msg_b = validar_matriz(data.matrix_b, "B") # Validar la matriz B
    if error_msg_b:
        raise HTTPException(status_code=400, detail=error_msg_b) # Lanzar excepción si hay un error en la matriz B

    # Verificar límites de tamaño antes de continuar
    if rows_a is not None and rows_a > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 filas. La matriz A tiene {rows_a} filas.")
    if cols_a is not None and cols_a > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 columnas. La matriz A tiene {cols_a} columnas.")
    if rows_b_val is not None and rows_b_val > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 filas. La matriz B tiene {rows_b_val} filas.")
    if cols_b_val is not None and cols_b_val > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 columnas. La matriz B tiene {cols_b_val} columnas.")

    matrix_b_frac: Matrix = [] # Inicializar la matriz B como una lista de listas de fracciones
    try:
        for i, row_b in enumerate(data.matrix_b): # Iterar sobre las filas de la matriz B
            row_b_frac = [] # Inicializar la fila como una lista de fracciones
            for j, val_b in enumerate(row_b): # Iterar sobre los valores de la fila
                row_b_frac.append(to_fraction(val_b)) # Convertir el valor a fracción y agregarlo a la fila
            matrix_b_frac.append(row_b_frac) # Agregar la fila a la matriz
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) # Lanzar excepción si hay un error de conversión

    steps.append("Matriz B ingresada:") # Agregar un paso al registro
    steps.extend(format_matrix_for_steps(matrix_b_frac, "Matriz B")) # Agregar la matriz B formateada a los pasos

    # Validar dimensiones para multiplicación
    valid_dims, dim_error_msg = validar_dimensiones_para_multiplicacion(matrix_a_frac, matrix_b_frac) # Validar las dimensiones de las matrices
    if not valid_dims:
        raise HTTPException(status_code=400, detail=dim_error_msg) # Lanzar excepción si las dimensiones no son válidas

    # Lógica de multiplicación
    rows_a = len(matrix_a_frac) # Obtener el número de filas de la matriz A
    cols_a = len(matrix_a_frac[0]) # Obtener el número de columnas de la matriz A (también es el número de filas de la matriz B)
    cols_b = len(matrix_b_frac[0]) # Obtener el número de columnas de la matriz B

    result_matrix_frac: Matrix = [[Fraction(0) for _ in range(cols_b)] for _ in range(rows_a)] # Inicializar la matriz resultante con ceros
    calculation_steps = [] # Inicializar la lista de pasos de cálculo

    steps.append("Proceso de multiplicación (A x B):") # Agregar un paso al registro
    for i in range(rows_a): # Iterar sobre las filas de la matriz A
        for j in range(cols_b): # Iterar sobre las columnas de la matriz B
            dot_product = Fraction(0) # Inicializar el producto punto
            step_detail = f"Elemento C[{i+1}][{j+1}] = " # Inicializar el detalle del paso
            calculation_parts = [] # Inicializar la lista de partes del cálculo
            for k in range(cols_a): # cols_a es igual a rows_b. Iterar sobre las columnas de A / filas de B
                term = matrix_a_frac[i][k] * matrix_b_frac[k][j] # Calcular el término
                dot_product += term # Sumar el término al producto punto
                calculation_parts.append(f"({format_fraction_output(matrix_a_frac[i][k])} * {format_fraction_output(matrix_b_frac[k][j])})") # Agregar el término formateado a las partes del cálculo
            step_detail += " + ".join(calculation_parts) # Unir las partes del cálculo con el signo de suma
            step_detail += f" = {format_fraction_output(dot_product)}" # Agregar el resultado formateado al detalle del paso
            calculation_steps.append(step_detail) # Agregar el detalle del paso a la lista de pasos de cálculo
            result_matrix_frac[i][j] = dot_product # Asignar el producto punto al elemento de la matriz resultante
    
    steps.extend(calculation_steps) # Agregar los pasos de cálculo a la lista de pasos
    steps.append("Matriz Resultante (C = A x B):") # Agregar un paso al registro
    steps.extend(format_matrix_for_steps(result_matrix_frac, "Matriz Resultante C")) # Agregar la matriz resultante formateada a los pasos

    # Formatear resultado para la API
    result_matrix_formatted = [ # Formatear la matriz resultante para la API
        [format_fraction_output(val) for val in row] # Formatear cada valor de la fila
        for row in result_matrix_frac # Iterar sobre las filas de la matriz resultante
    ]

    return ApiResponse( # Retornar la respuesta de la API
        success=True, # Indicar que la operación fue exitosa
        result=result_matrix_formatted, # Agregar la matriz resultante formateada
        steps=steps # Agregar los pasos
    )