from fastapi import APIRouter, HTTPException
from typing import List, Tuple, Union
from fractions import Fraction

from backend.models import SystemInput, ApiResponse, MatrixElement
from backend.utils.type_converters import to_fraction, format_fraction_output
from backend.utils.formatters import format_matrix_for_steps, format_augmented_matrix_for_steps
from backend.utils.validators import validar_matriz

router = APIRouter()

def _solve_gaussian_elimination(
    matrix_a_frac: List[List[Fraction]], 
    vector_b_frac: List[Fraction], 
    steps_ref: List[str]
) -> Tuple[Union[List[Fraction], None], str, bool]:
    """
    Resuelve un sistema de ecuaciones lineales Ax=b usando Eliminación Gaussiana.
    Transforma la matriz aumentada [A|b] a forma escalonada por filas.
    Luego realiza sustitución hacia atrás si hay solución única.
    
    Retorna:
        - solution (List[Fraction] | None): El vector solución si es única, None en otros casos.
        - message (str): Mensaje indicando el tipo de solución (única, múltiple, sin solución).
        - success (bool): True si se encontró una solución (aunque sea para indicar múltiples o ninguna), False si hubo error irrecuperable.
    """
    n = len(matrix_a_frac)
    if n == 0:
        return None, "La matriz de coeficientes A no puede estar vacía.", False
    if len(matrix_a_frac[0]) != n: # Asumimos que validar_matriz ya verificó rectangularidad
        return None, "La matriz de coeficientes A debe ser cuadrada para este método simplificado de solución única.", False # Simplificando, por ahora
    if len(vector_b_frac) != n:
        return None, f"El vector b debe tener {n} elementos, pero tiene {len(vector_b_frac)}.", False

    # Formar la matriz aumentada [A|b]
    augmented_matrix = [matrix_a_frac[i] + [vector_b_frac[i]] for i in range(n)]
    steps_ref.append("Matriz aumentada inicial [A|b]:")
    steps_ref.extend(format_augmented_matrix_for_steps(augmented_matrix, n, f"Aumentada ({n}x{n+1})"))

    # Fase de eliminación (hacia adelante) para obtener forma escalonada por filas
    for h in range(n):  # h es la fila y columna del pivote actual
        # Encontrar la fila con el pivote máximo en la columna h (desde la fila h hacia abajo)
        pivot_row = h
        for i in range(h + 1, n):
            if abs(augmented_matrix[i][h]) > abs(augmented_matrix[pivot_row][h]):
                pivot_row = i
        
        # Intercambiar filas si es necesario
        if pivot_row != h:
            augmented_matrix[h], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[h]
            steps_ref.append(f"Intercambiando Fila {h+1} con Fila {pivot_row+1} para obtener un pivote más grande (o no nulo) en A({h+1},{h+1}).")
            steps_ref.extend(format_augmented_matrix_for_steps(augmented_matrix, n, "Matriz aumentada después del intercambio"))

        # Verificar si el pivote es cero (lo que podría indicar singularidad o dependencia lineal)
        if augmented_matrix[h][h] == 0:
            # Si hay un elemento no cero en la columna de constantes b para esta fila, entonces no hay solución
            if augmented_matrix[h][n] != 0:
                steps_ref.append(f"Fila {h+1} de la matriz escalonada es [0 ... 0 | {format_fraction_output(augmented_matrix[h][n])}] donde el término constante no es cero.")
                steps_ref.append("Esto indica una inconsistencia.")
                return None, "El sistema no tiene solución (es inconsistente).", True 
            # Si el pivote es cero y la constante también es cero, podría haber soluciones infinitas
            # o podría ser una fila de ceros que no aporta información.
            # Para simplificar, si llegamos a un pivote cero aquí, asumimos dependencia y potencial para infinitas soluciones,
            # a menos que una inconsistencia anterior lo haya descartado.
            # Esta lógica necesitaría ser más robusta para caracterizar completamente las soluciones infinitas.
            continue # Avanzar a la siguiente fila, puede haber una fila de ceros.

        pivot_element = augmented_matrix[h][h]
        steps_ref.append(f"Pivote actual A({h+1},{h+1}) = {format_fraction_output(pivot_element)}")

        # Eliminar elementos debajo del pivote
        for i in range(h + 1, n):
            if augmented_matrix[i][h] != 0:
                factor = augmented_matrix[i][h] / pivot_element
                operation_description = f"F{i+1} = F{i+1} - ({format_fraction_output(factor)}) * F{h+1}"
                steps_ref.append(f"Eliminando elemento A({i+1},{h+1}) usando la operación: {operation_description}")
                
                for j in range(h, n + 1): # Incluir la columna de constantes b
                    augmented_matrix[i][j] -= factor * augmented_matrix[h][j]
                steps_ref.extend(format_augmented_matrix_for_steps(augmented_matrix, n, "Matriz aumentada después de la operación"))

    steps_ref.append("Matriz en forma escalonada por filas:")
    steps_ref.extend(format_augmented_matrix_for_steps(augmented_matrix, n, "Forma Escalonada"))

    # Verificar consistencia y número de soluciones
    rank_a = 0
    for i in range(n):
        is_zero_row_a = all(augmented_matrix[i][j] == 0 for j in range(n))
        if not is_zero_row_a:
            rank_a +=1
        elif augmented_matrix[i][n] != 0: # Fila [0 0 ... 0 | c] con c != 0
            steps_ref.append(f"Fila {i+1} ([0...0 | {format_fraction_output(augmented_matrix[i][n])}]) indica que el sistema es inconsistente.")
            return None, "El sistema no tiene solución (es inconsistente).", True

    if rank_a < n:
        steps_ref.append(f"El rango de la matriz de coeficientes ({rank_a}) es menor que el número de variables ({n}).")
        steps_ref.append("El sistema tiene soluciones infinitas (si es consistente).")
        # Para este ejercicio, no se calculará la forma paramétrica de las soluciones infinitas.
        return None, "El sistema tiene soluciones infinitas.", True

    # Fase de sustitución hacia atrás (solo si hay solución única, rank_a == n)
    solution = [Fraction(0) for _ in range(n)]
    steps_ref.append("Iniciando sustitución hacia atrás para encontrar la solución:")
    for i in range(n - 1, -1, -1):
        sum_ax = Fraction(0)
        for j in range(i + 1, n):
            sum_ax += augmented_matrix[i][j] * solution[j]
        
        if augmented_matrix[i][i] == 0:
             # Esto no debería ocurrir si rank_a == n y no hubo inconsistencia previa.
             # Podría ocurrir si el sistema es singular y rank_a < n pero se omitió el chequeo.
             steps_ref.append(f"Error: Elemento diagonal A({i+1},{i+1}) es cero durante la sustitución hacia atrás y se esperaba solución única.")
             return None, "Error durante la sustitución hacia atrás, posible sistema singular no detectado antes.", False

        solution[i] = (augmented_matrix[i][n] - sum_ax) / augmented_matrix[i][i]
        sum_ax_str = format_fraction_output(sum_ax)
        const_term_str = format_fraction_output(augmented_matrix[i][n])
        pivot_val_str = format_fraction_output(augmented_matrix[i][i])
        sol_i_str = format_fraction_output(solution[i])
        variable_name = f"x{i+1}" # o x, y, z, w
        if n <= 4: variable_name = ['x', 'y', 'z', 'w'][i]

        if n - (i+1) > 0: # Si hay términos en sum_ax
            steps_ref.append(f"  De Fila {i+1}: {pivot_val_str}*{variable_name} + ... = {const_term_str}")
            steps_ref.append(f"  {pivot_val_str}*{variable_name} = {const_term_str} - ({sum_ax_str}) = {format_fraction_output(augmented_matrix[i][n] - sum_ax)}")
            steps_ref.append(f"  {variable_name} = {format_fraction_output(augmented_matrix[i][n] - sum_ax)} / {pivot_val_str} = {sol_i_str}")
        else: # Última variable o sistema 1x1
            steps_ref.append(f"  De Fila {i+1}: {pivot_val_str}*{variable_name} = {const_term_str}")
            steps_ref.append(f"  {variable_name} = {const_term_str} / {pivot_val_str} = {sol_i_str}")

    steps_ref.append("Sustitución hacia atrás completada.")
    return solution, "El sistema tiene una solución única.", True

@router.post("/solve_system_gaussian", response_model=ApiResponse, summary="Resuelve un sistema Ax=b usando Eliminación Gaussiana")
async def solve_system_gaussian_endpoint(data: SystemInput):
    steps: List[str] = []

    # 1. Validar Matriz A
    rows_a, cols_a, error_msg_a = validar_matriz(data.matrix_a, "A")
    if error_msg_a:
        raise HTTPException(status_code=400, detail=f"Error en Matriz A: {error_msg_a}")
    
    if rows_a is None or cols_a is None: # Salvaguarda
        raise HTTPException(status_code=400, detail="Error al obtener dimensiones de la matriz A.")

    # Validar Vector b (como una matriz de N x 1 conceptualmente para validación)
    matrix_b_for_validation: List[List[MatrixElement]] = [[el] for el in data.vector_b] # Primero convertir
    rows_b, _, error_msg_b = validar_matriz(matrix_b_for_validation, "Vector b", expected_cols=1) # _ para cols_b ya que sabemos que es 1
    if error_msg_b:
        # Usamos un nombre más descriptivo para el error de vector b si falla la validación de forma
        if "no puede estar vacía" in error_msg_b and not data.vector_b:
             error_msg_b = "El vector b no puede estar vacío."
        elif "debe tener 1 columnas" in error_msg_b: # Mensaje de expected_cols
            error_msg_b = "El vector b no se pudo interpretar como un vector columna (error de forma interna)."
        elif "cero filas" in error_msg_b and not data.vector_b:
             error_msg_b = "El vector b no puede estar vacío (cero elementos)."
        else: # Otros errores de validar_matriz (e.g. elementos no son listas, etc.)
            error_msg_b = f"Vector b: {error_msg_b}" # Mantiene el mensaje original con prefijo
        raise HTTPException(status_code=400, detail=f"Error en Vector b: {error_msg_b}")

    if rows_b is None : # Salvaguarda post-validación vector b
        raise HTTPException(status_code=400, detail="Error al obtener dimensión del vector b.")

    # Validaciones específicas de dimensiones para Ax=b
    if rows_a != rows_b:
        raise HTTPException(status_code=400, detail=f"El número de filas de la matriz A ({rows_a}) debe coincidir con el número de elementos del vector b ({rows_b}).")
    if cols_a > 4 or rows_a > 4: # Mantenemos límite de 4x4 para A
        raise HTTPException(status_code=400, detail=f"La matriz A está limitada a dimensiones de hasta 4x4. Se recibió {rows_a}x{cols_a}.")

    # ---- Aquí comienzan las conversiones y el log de pasos ----
    # 2. Conversión a Fracciones y registro inicial de pasos
    matrix_a_frac: List[List[Fraction]] = []
    vector_b_frac: List[Fraction] = []
    try:
        for i, row_data in enumerate(data.matrix_a):
            # Esta validación de ragged es redundante si validar_matriz funcionó bien,
            # pero es una salvaguarda por si acaso y para ser explícitos.
            if len(row_data) != cols_a:
                raise ValueError(f"La fila {i+1} de la matriz A tiene {len(row_data)} elementos, se esperaban {cols_a}.")
            matrix_a_frac.append([to_fraction(val) for val in row_data])
        
        for val_b in data.vector_b: # Usar data.vector_b directamente para la conversión
            vector_b_frac.append(to_fraction(val_b))

    except ValueError as e: # Captura errores de to_fraction
        raise HTTPException(status_code=400, detail=f"Error de conversión de valor: {str(e)}")

    # Agregar pasos iniciales DESPUÉS de las validaciones y conversiones principales
    steps.append("Sistema de ecuaciones Ax=b:")
    steps.append("Matriz de coeficientes A:")
    steps.extend(format_matrix_for_steps(matrix_a_frac, f"A ({rows_a}x{cols_a})"))
    steps.append("Vector de constantes b:")
    vector_b_display = [[el] for el in vector_b_frac] # Formatear b como columna para mostrar
    steps.extend(format_matrix_for_steps(vector_b_display, f"b ({rows_b}x1)"))

    # ---- Fin de validaciones críticas que deben ser HTTPException ----
    # ---- Comienzo de lógica de resolución donde _solve_gaussian_elimination puede retornar success=False ----

    # CHEQUEO ESPECÍFICO PARA MATRIZ A CUADRADA ANTES DE LLAMAR A _solve_gaussian_elimination
    # _solve_gaussian_elimination actualmente asume A cuadrada.
    if rows_a != cols_a:
        # Este error es específico de la implementación actual de _solve_gaussian_elimination
        # que no maneja sistemas no cuadrados. Se devuelve como HTTPException porque es una
        # precondición para la lógica de resolución actual.
        raise HTTPException(status_code=400, detail="La matriz de coeficientes A debe ser cuadrada para este método simplificado de solución única.")

    # 3. Resolver usando Eliminación Gaussiana
    solution_frac, message, success_solve = _solve_gaussian_elimination(matrix_a_frac, vector_b_frac, steps)

    if not success_solve: # Error interno durante la resolución o caso no manejado como éxito (e.g. no cuadrada en _solve)
        # Si _solve_gaussian_elimination devuelve success_solve=False, el mensaje ya indica el problema.
        return ApiResponse(success=False, error=message, steps=steps) # Este error ya no debería ser por A no cuadrada si se chequeó antes

    if solution_frac:
        formatted_solution = [format_fraction_output(val) for val in solution_frac]
        steps.append("Solución del sistema x:")
        # Formatear x como una matriz columna para mostrar
        solution_display = [[el] for el in formatted_solution]
        steps.extend(format_matrix_for_steps(solution_display, f"x ({rows_a}x1)"))
        
        return ApiResponse(success=True, result={"solution_vector": formatted_solution, "message": message}, steps=steps)
    else:
        # Casos de no solución o múltiples soluciones
        return ApiResponse(success=True, result={"message": message}, steps=steps, error=(message if "no tiene solución" in message else None) ) 