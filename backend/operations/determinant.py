from fastapi import APIRouter, HTTPException
from typing import List
from fractions import Fraction

from backend.models import MatrixInput, ApiResponse, Matrix
from backend.utils.type_converters import to_fraction, format_fraction_output
from backend.utils.formatters import format_matrix_for_steps
from backend.utils.validators import validar_matriz

router = APIRouter()

def _calculate_determinant_gaussian(matrix_input: List[List[Fraction]], steps_ref: List[str]) -> Fraction:
    """
    Calcula el determinante de una matriz utilizando eliminación Gaussiana.
    Transforma la matriz a una forma triangular superior.
    Añade pasos detallados del cálculo a steps_ref.
    """
    # Crear una copia profunda para evitar modificar la lista de listas original si se pasa por referencia
    matrix = [[val for val in row] for row in matrix_input]
    n = len(matrix) # Obtiene la dimensión de la matriz (asumiendo que es cuadrada)
    determinant_multiplier = Fraction(1) # Inicializa el multiplicador del determinante para los intercambios de filas

    steps_ref.append("Transformando la matriz a forma triangular superior mediante eliminación Gaussiana:")

    for h in range(n):  # h es el índice de la fila y columna del pivote actual
        # Encontrar pivote para esta columna
        pivot_row = -1 # Inicializa el índice de la fila pivote
        for i in range(h, n): # Busca una fila con un valor no nulo en la columna h, desde la fila h hasta el final
            if matrix[i][h] != 0:
                pivot_row = i # Si encuentra un valor no nulo, actualiza el índice de la fila pivote
                break
        
        if pivot_row == -1:
            # Si no hay pivote en esta columna (todos son ceros debajo/en la diagonal), el determinante es 0
            steps_ref.append(f"Columna {h+1} (debajo o en la diagonal) no tiene pivote (todos son cero).")
            steps_ref.append("El determinante es 0.")
            return Fraction(0) # Retorna 0 como el determinante

        # Intercambiar filas si es necesario para mover el pivote a la diagonal
        if pivot_row != h:
            matrix[h], matrix[pivot_row] = matrix[pivot_row], matrix[h] # Intercambia la fila actual con la fila pivote
            determinant_multiplier *= -1 # Actualiza el multiplicador del determinante (cambia de signo)
            steps_ref.append(f"Intercambiando Fila {h+1} con Fila {pivot_row+1} para obtener un pivote no nulo en A({h+1},{h+1}).")
            steps_ref.append(f"  (Multiplicador del determinante actual: {format_fraction_output(determinant_multiplier)})")
            steps_ref.extend(format_matrix_for_steps(matrix, "Matriz después del intercambio"))

        # Eliminar otras filas
        # El elemento pivote es matrix[h][h]
        pivot_element = matrix[h][h] # Obtiene el valor del elemento pivote
        steps_ref.append(f"Pivote actual A({h+1},{h+1}) = {format_fraction_output(pivot_element)}")

        for i in range(h + 1, n): # Para todas las filas debajo del pivote
            if matrix[i][h] != 0: # Si el elemento debajo del pivote no es cero
                factor = matrix[i][h] / pivot_element # Calcula el factor para eliminar el elemento
                operation_description = f"F{i+1} = F{i+1} - ({format_fraction_output(factor)}) * F{h+1}" # Describe la operación de fila
                steps_ref.append(f"Eliminando elemento A({i+1},{h+1}) usando la operación: {operation_description}")
                
                # Aplicar operación de fila
                for j in range(h, n): # Iterar a través de las columnas de la fila actual
                    matrix[i][j] -= factor * matrix[h][j] # Aplica la operación de fila para eliminar el elemento
                
                steps_ref.extend(format_matrix_for_steps(matrix, "Matriz después de la operación"))

    # La matriz ahora está en forma triangular superior. El determinante es el producto de los elementos diagonales * multiplicador
    steps_ref.append("La matriz está en forma triangular superior.")
    steps_ref.extend(format_matrix_for_steps(matrix, "Matriz triangular superior final"))

    determinant_value = determinant_multiplier # Inicializa el valor del determinante con el multiplicador
    diag_product_str_parts = []
    for i in range(n):
        determinant_value *= matrix[i][i] # Multiplica el determinante por el elemento diagonal
        diag_product_str_parts.append(format_fraction_output(matrix[i][i])) # Guarda el elemento diagonal formateado para mostrar
    
    diag_product_str = " * ".join(diag_product_str_parts) # Une los elementos diagonales formateados con " * "
    if n > 0 :
        steps_ref.append(f"Calculando el determinante como el producto de los elementos de la diagonal multiplicados por el factor de intercambio de filas ({format_fraction_output(determinant_multiplier)}):")
        steps_ref.append(f"  det(A) = {format_fraction_output(determinant_multiplier)} * ({diag_product_str})")
        steps_ref.append(f"         = {format_fraction_output(determinant_multiplier)} * {format_fraction_output(determinant_value / determinant_multiplier if determinant_multiplier != 0 else 0)}") # producto de la diagonal
        steps_ref.append(f"         = {format_fraction_output(determinant_value)}")
    else: # No debería ocurrir debido a las validaciones
        steps_ref.append("La matriz es 0x0, el determinante es 1 por convención (o 0 si se considera inválido).")
        determinant_value = Fraction(1) # O 0, depende de la convención para matriz vacía. Las validaciones previenen esto.

    return determinant_value

@router.post("/determinant", response_model=ApiResponse, summary="Cálculo de determinante de una matriz usando Eliminación Gaussiana")
async def calculate_determinant_endpoint(data: MatrixInput):
    steps: List[str] = []

    # 1. Validación
    rows, cols, error_msg_val = validar_matriz(data.matrix, "suministrada") 
    if error_msg_val:
        raise HTTPException(status_code=400, detail=error_msg_val)
    
    # rows y cols ahora están garantizados de no ser None por validar_matriz si error_msg_val es None
    # Agregar verificaciones específicas de tamaño y cuadradas para la operación de determinante
    if rows is None or cols is None: # No debería ocurrir si error_msg_val es None, pero como salvaguarda
        raise HTTPException(status_code=400, detail="Error al obtener dimensiones de la matriz.")

    if rows > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 filas. Se recibió una matriz con {rows} filas.")
    if cols > 4:
        raise HTTPException(status_code=400, detail=f"La operación está limitada a matrices de hasta 4 columnas. Se recibió una matriz con {cols} columnas.")
    if rows != cols:
        raise HTTPException(status_code=400, detail=f"La matriz debe ser cuadrada para calcular el determinante. Se recibió una matriz de {rows}x{cols}.")
    
    n = rows # Tamaño de la matriz cuadrada

    # 2. Conversión de tipo
    matrix_a_frac: List[List[Fraction]] = []
    try:
        for i, row_data in enumerate(data.matrix):
            if len(row_data) != n: # Redundante si validar_matriz verifica rectangularidad
                 raise ValueError(f"La fila {i+1} tiene {len(row_data)} elementos, se esperaban {n}.")
            matrix_a_frac.append([to_fraction(val) for val in row_data])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    steps.append("Matriz de entrada A:")
    steps.extend(format_matrix_for_steps(matrix_a_frac, f"A ({n}x{n})"))

    # 3. Cálculo del determinante usando eliminación Gaussiana
    determinant_value: Fraction
    
    if n == 0: # Debería ser detectado por validar_matriz
        determinant_value = Fraction(1) # O 0, por convención. validar_matriz debería prevenir esto.
        steps.append("La matriz está vacía. El determinante de una matriz 0x0 es 1 por convención.")
    elif n == 1:
        determinant_value = matrix_a_frac[0][0]
        steps.append(f"La matriz es 1x1. El determinante es el único elemento: det(A) = {format_fraction_output(determinant_value)}")
    else: # n > 1 (es decir, 2x2, 3x3, 4x4)
        determinant_value = _calculate_determinant_gaussian(matrix_a_frac, steps)

    # 4. Formatear salida
    formatted_determinant = format_fraction_output(determinant_value)
    
    steps.append(f"El determinante final (calculado mediante eliminación Gaussiana) de la matriz A es: {formatted_determinant}")

    return ApiResponse(
        success=True,
        result=formatted_determinant,
        steps=steps
    ) 