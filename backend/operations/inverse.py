from fastapi import APIRouter, HTTPException
from typing import List, Tuple
from fractions import Fraction

from backend.models import MatrixInput, ApiResponse, Matrix
from backend.utils.type_converters import to_fraction, format_fraction_output
from backend.utils.formatters import format_matrix_for_steps
from backend.utils.validators import validar_matriz

router = APIRouter()

def _gauss_jordan_inverse(matrix_input: List[List[Fraction]], steps_ref: List[str]) -> Tuple[List[List[Fraction]] | None, bool]:
    """
    Calcula la inversa de una matriz utilizando eliminación de Gauss-Jordan.
    Aumenta la matriz con una matriz identidad [A|I] y la transforma a [I|A^-1].
    Retorna la matriz inversa y un booleano indicando si es invertible.
    Añade pasos detallados del cálculo a steps_ref.
    """
    n = len(matrix_input)
    # Crear una copia profunda para evitar modificar la lista de listas original
    matrix_a = [[val for val in row] for row in matrix_input]

    # Aumentar con matriz identidad
    identity_matrix = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
    augmented_matrix = [matrix_a[i] + identity_matrix[i] for i in range(n)]
    
    steps_ref.append("Matriz aumentada inicial [A|I]:")
    steps_ref.extend(format_matrix_for_steps(augmented_matrix, f"Augmented ({n}x{2*n})"))

    # Realizar eliminación Gaussiana para obtener [I|A^-1]
    for h in range(n):  # h es el índice de la fila y columna del pivote actual
        # Encontrar pivote para esta columna
        pivot_row = -1
        for i in range(h, n):
            if augmented_matrix[i][h] != 0:
                pivot_row = i
                break
        
        if pivot_row == -1:
            steps_ref.append(f"No se encontró pivote no nulo en la columna {h+1} (después de procesar filas anteriores).")
            steps_ref.append("La matriz no es invertible (singular).")
            return None, False # No es invertible

        # Intercambiar filas si es necesario para mover el pivote a la diagonal
        if pivot_row != h:
            augmented_matrix[h], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[h]
            steps_ref.append(f"Intercambiando Fila {h+1} con Fila {pivot_row+1} para obtener un pivote no nulo en A({h+1},{h+1}).")
            steps_ref.extend(format_matrix_for_steps(augmented_matrix, "Matriz aumentada después del intercambio"))

        # Normalizar fila del pivote (hacer que el elemento pivote sea 1)
        pivot_element = augmented_matrix[h][h]
        if pivot_element != 1:
            if pivot_element == 0: # Debería ser detectado por pivot_row == -1, pero como salvaguarda
                 steps_ref.append(f"Error: Pivote en A({h+1},{h+1}) es cero inesperadamente.")
                 steps_ref.append("La matriz no es invertible (singular).")
                 return None, False
            
            steps_ref.append(f"Normalizando Fila {h+1}: F{h+1} = F{h+1} / {format_fraction_output(pivot_element)}")
            for j in range(2 * n): # Iterar por todas las columnas de la matriz aumentada
                augmented_matrix[h][j] /= pivot_element
            
            steps_ref.extend(format_matrix_for_steps(augmented_matrix, f"Matriz aumentada después de normalizar F{h+1}"))
        
        steps_ref.append(f"Pivote en A({h+1},{h+1}) es 1.")

        # Eliminar otras filas (hacer que otros elementos en la columna pivote sean cero)
        for i in range(n):
            if i != h: # Para todas las filas excepto la fila pivote
                if augmented_matrix[i][h] != 0: # Si el elemento en la columna pivote no es cero
                    factor = augmented_matrix[i][h]
                    operation_description = f"F{i+1} = F{i+1} - ({format_fraction_output(factor)}) * F{h+1}"
                    steps_ref.append(f"Eliminando elemento A({i+1},{h+1}) usando la operación: {operation_description}")
                    
                    for j in range(h, 2 * n): # Iterar por las columnas relevantes
                        augmented_matrix[i][j] -= factor * augmented_matrix[h][j]
                    
                    steps_ref.extend(format_matrix_for_steps(augmented_matrix, f"Matriz aumentada después de la operación en F{i+1}"))

    # Verificar si el lado izquierdo es una matriz identidad
    for i in range(n):
        for j in range(n):
            if (i == j and augmented_matrix[i][j] != 1) or \
               (i != j and augmented_matrix[i][j] != 0):
                steps_ref.append("La parte izquierda de la matriz aumentada no es la matriz identidad después de la eliminación.")
                steps_ref.append("La matriz no es invertible (singular).")
                return None, False

    # Extraer matriz inversa
    inverse_matrix = [row[n:] for row in augmented_matrix]
    steps_ref.append("Proceso de eliminación de Gauss-Jordan completado.")
    steps_ref.append("La parte izquierda es la matriz identidad, la parte derecha es la inversa A⁻¹.")
    steps_ref.extend(format_matrix_for_steps(inverse_matrix, "Matriz Inversa A⁻¹"))
    return inverse_matrix, True


@router.post("/inverse", response_model=ApiResponse, summary="Cálculo de la inversa de una matriz usando Gauss-Jordan")
async def calculate_inverse_endpoint(data: MatrixInput):
    steps: List[str] = []

    # 1. Validación
    rows, cols, error_msg_val = validar_matriz(data.matrix, "suministrada")
    if error_msg_val:
        raise HTTPException(status_code=400, detail=error_msg_val)
    
    if rows is None or cols is None:
        raise HTTPException(status_code=400, detail="Error al obtener dimensiones de la matriz.")

    if rows > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 filas. Se recibió una matriz con {rows} filas.")
    if cols > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 columnas. Se recibió una matriz con {cols} columnas.")
    if rows != cols:
        raise HTTPException(status_code=400, detail=f"La matriz debe ser cuadrada para calcular su inversa. Se recibió una matriz de {rows}x{cols}.")
    
    n = rows

    # 2. Conversión de tipos
    matrix_a_frac: List[List[Fraction]] = []
    try:
        for i, row_data in enumerate(data.matrix):
            matrix_a_frac.append([to_fraction(val) for val in row_data])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    steps.append("Matriz de entrada A:")
    steps.extend(format_matrix_for_steps(matrix_a_frac, f"A ({n}x{n})"))

    # 3. Cálculo de la inversa usando Gauss-Jordan
    if n == 0: # Debería ser detectado por validar_matriz
        raise HTTPException(status_code=400, detail="No se puede calcular la inversa de una matriz vacía.")

    inverse_matrix_frac, is_invertible = _gauss_jordan_inverse(matrix_a_frac, steps)

    if not is_invertible:
        # Los pasos para la no invertibilidad ya han sido añadidos por _gauss_jordan_inverse
        return ApiResponse(
            success=False,
            error="La matriz no es invertible (singular). Los pasos detallan el problema.",
            steps=steps,
            result=None # Establecer explícitamente el resultado como None o una lista vacía
        )

    # 4. Formatear salida
    if inverse_matrix_frac is None: # No debería ocurrir si is_invertible es True
        # Este caso idealmente debería estar cubierto por la verificación is_invertible.
        # Añadido como salvaguarda.
        steps.append("Error inesperado: La matriz fue marcada como invertible pero no se generó la inversa.")
        return ApiResponse(success=False, error="Error interno al calcular la inversa.", steps=steps)

    formatted_inverse_matrix = [
        [format_fraction_output(val) for val in row] 
        for row in inverse_matrix_frac
    ]
    
    steps.append("La inversa de la matriz A ha sido calculada exitosamente.")

    return ApiResponse(
        success=True,
        result=formatted_inverse_matrix,
        steps=steps
    ) 