from fastapi import APIRouter, HTTPException
from typing import List, Tuple, Optional
from fractions import Fraction

from backend.models import SystemInput, ApiResponse, Matrix, OutputMatrix
from backend.utils.type_converters import to_fraction, format_fraction_output
from backend.utils.formatters import format_matrix_for_steps
from backend.utils.validators import validar_matriz, validar_vector

router = APIRouter()

def _gauss_jordan_elimination(
    matrix_a_frac: Matrix, 
    vector_b_frac: List[Fraction], 
    steps_ref: List[str]
) -> Tuple[Optional[OutputMatrix], Optional[List[str]], str, bool, Optional[str]]:
    """
    Resuelve un sistema Ax=b usando eliminación de Gauss-Jordan.
    Returns: RREF_matrix, solution_vector, message, rref_calculation_success, error_detail
    rref_calculation_success is True if RREF could be calculated.
    message describes the system's solution type.
    error_detail is for issues like "no solution", "infinite solutions", or core calculation errors.
    """
    n_rows = len(matrix_a_frac) # Obtiene el número de filas de la matriz A
    if n_rows == 0: # Si la matriz A está vacía
        return None, None, "Error: Matriz A no puede ser vacía.", False, "Matriz A vacía."
    
    n_cols_a = 0
    if matrix_a_frac and matrix_a_frac[0]: # Verifica si la primera fila existe y no está vacía
        n_cols_a = len(matrix_a_frac[0]) # Obtiene el número de columnas de la matriz A
    
    if n_cols_a == 0: # Maneja el caso si matrix_a_frac es [[]] o similar
         return None, None, "Error: Matriz A no puede tener cero columnas.", False, "Matriz A sin columnas."

    augmented_matrix: Matrix = [row[:] + [vector_b_frac[i]] for i, row in enumerate(matrix_a_frac)] # Crea la matriz aumentada [A|b]
    n_cols_aug = n_cols_a + 1 # Calcula el número de columnas de la matriz aumentada
    
    steps_ref.append("Matriz aumentada inicial [A|b]:") # Agrega un mensaje a los pasos
    steps_ref.extend(format_matrix_for_steps(augmented_matrix, f"Aumentada ({n_rows}x{n_cols_aug})")) # Agrega la matriz aumentada formateada a los pasos

    pivot_row = 0 # Inicializa la fila del pivote
    for col in range(n_cols_a): # Itera sobre las columnas de la matriz A
        if pivot_row >= n_rows: break # Si la fila del pivote es mayor o igual al número de filas, termina el bucle

        i_max = pivot_row # Inicializa el índice de la fila con el valor absoluto máximo
        for i in range(pivot_row + 1, n_rows): # Itera sobre las filas debajo de la fila del pivote
            if abs(augmented_matrix[i][col]) > abs(augmented_matrix[i_max][col]): # Si el valor absoluto del elemento actual es mayor que el valor absoluto del elemento máximo actual
                i_max = i # Actualiza el índice de la fila con el valor absoluto máximo
        
        # Usando un número muy pequeño para verificar el cero efectivo para el pivote
        # Esta tolerancia podría necesitar ajuste dependiendo de la precisión esperada
        if abs(augmented_matrix[i_max][col]) < Fraction(1, 10**12): # Si el valor absoluto del elemento máximo es menor que la tolerancia
            steps_ref.append(f"  Pivote en columna {col+1} (para A({pivot_row+1},{col+1})) es cero o insignificante. Saltando esta columna.") # Agrega un mensaje a los pasos
            continue # Salta a la siguiente columna

        if i_max != pivot_row: # Si el índice de la fila con el valor absoluto máximo no es igual a la fila del pivote
            augmented_matrix[pivot_row], augmented_matrix[i_max] = augmented_matrix[i_max], augmented_matrix[pivot_row] # Intercambia las filas
            steps_ref.append(f"  Intercambiando Fila {pivot_row+1} con Fila {i_max+1}.") # Agrega un mensaje a los pasos
            steps_ref.extend(format_matrix_for_steps(augmented_matrix, "Después de intercambio")) # Agrega la matriz aumentada formateada a los pasos

        pivot_element = augmented_matrix[pivot_row][col] # Obtiene el elemento pivote
        if pivot_element != 1: # Si el elemento pivote no es 1
            steps_ref.append(f"  Normalizando Fila {pivot_row+1}: F{pivot_row+1} = F{pivot_row+1} / {format_fraction_output(pivot_element)}") # Agrega un mensaje a los pasos
            for j in range(col, n_cols_aug): # Itera sobre las columnas desde la columna del pivote hasta el final de la fila
                augmented_matrix[pivot_row][j] /= pivot_element # Divide cada elemento de la fila por el elemento pivote
            steps_ref.extend(format_matrix_for_steps(augmented_matrix, "Después de normalizar")) # Agrega la matriz aumentada formateada a los pasos
        
        for i in range(n_rows): # Itera sobre las filas
            if i != pivot_row: # Si la fila actual no es la fila del pivote
                factor = augmented_matrix[i][col] # Obtiene el factor para eliminar
                if factor != 0: # Si el factor no es cero
                    steps_ref.append(f"  Eliminando en Fila {i+1}: F{i+1} = F{i+1} - ({format_fraction_output(factor)}) * F{pivot_row+1}") # Agrega un mensaje a los pasos
                    for j in range(col, n_cols_aug): # Itera sobre las columnas desde la columna del pivote hasta el final de la fila
                        augmented_matrix[i][j] -= factor * augmented_matrix[pivot_row][j] # Elimina el elemento
                    steps_ref.extend(format_matrix_for_steps(augmented_matrix, f"Después de F{i+1}")) # Agrega la matriz aumentada formateada a los pasos
        pivot_row += 1 # Incrementa la fila del pivote

    rref_output = [[format_fraction_output(el) for el in r_row] for r_row in augmented_matrix] # Formatea la matriz aumentada en forma escalonada reducida
    steps_ref.append("Forma escalonada reducida por filas (RREF) de la matriz aumentada:") # Agrega un mensaje a los pasos
    steps_ref.extend(format_matrix_for_steps(rref_output, f"RREF ({n_rows}x{n_cols_aug})")) # Agrega la matriz en forma escalonada reducida formateada a los pasos
    
    rank_A = 0 # Inicializa el rango de A
    # Cálculo más robusto del rango: cuenta las filas no nulas en la parte A de RREF, o el número de columnas pivote encontradas
    # La variable 'pivot_row' del bucle representa correctamente el rango de la matriz A.
    rank_A = pivot_row # El rango de A es igual al número de filas pivote

    # Verifica la inconsistencia: 0 = k donde k != 0
    for i in range(rank_A, n_rows): # Verifica las filas que deberían ser todas cero en la parte A
        if all(augmented_matrix[i][j] == 0 for j in range(n_cols_a)) and augmented_matrix[i][n_cols_a] != 0: # Si todos los elementos en la parte A son cero y el elemento en la parte b no es cero
            msg = "El sistema no tiene solución (es inconsistente)." # El sistema no tiene solución
            err_detail = msg # El detalle del error es el mensaje
            steps_ref.append(f"  Fila {i+1} de RREF ({rref_output[i]}) indica inconsistencia (0 = {rref_output[i][n_cols_a]}).") # Agrega un mensaje a los pasos
            steps_ref.append(msg) # Agrega el mensaje a los pasos
            return rref_output, None, msg, True, err_detail # Retorna la matriz en forma escalonada reducida, None, el mensaje, True y el detalle del error

    # Verifica si hay soluciones infinitas: rank_A < número de variables (n_cols_a)
    if rank_A < n_cols_a: # Si el rango de A es menor que el número de columnas de A
        msg = "El sistema tiene soluciones infinitas." # El sistema tiene soluciones infinitas
        steps_ref.append(f"  Hay {rank_A} pivotes (rango de A) y {n_cols_a} variables. Como ({rank_A} < {n_cols_a}) y el sistema es consistente.") # Agrega un mensaje a los pasos
        steps_ref.append(msg) # Agrega el mensaje a los pasos
        return rref_output, None, msg, True, None # No hay un error específico para la API, el mensaje en el resultado lo cubre

    # Verifica si hay una solución única: rank_A == número de variables
    if rank_A == n_cols_a: # Si el rango de A es igual al número de columnas de A
        # Esto implica que rank_A también es <= n_rows. Si el sistema es consistente.
        solution_vector_frac = [augmented_matrix[i][n_cols_a] for i in range(n_cols_a)] # Asume que n_cols_a <= n_rows después de RREF
        output_solution_list_str = [format_fraction_output(val) for val in solution_vector_frac] # Formatea el vector solución
        msg = "El sistema tiene una solución única." # El sistema tiene una solución única
        steps_ref.append(msg) # Agrega el mensaje a los pasos
        steps_ref.append("Vector solución x:") # Agrega un mensaje a los pasos
        solution_for_steps = [[val] for val in output_solution_list_str] # Crea una matriz para los pasos
        steps_ref.extend(format_matrix_for_steps(solution_for_steps, f"x ({n_cols_a}x1)")) # Agrega el vector solución formateado a los pasos
        return rref_output, output_solution_list_str, msg, True, None # Retorna la matriz en forma escalonada reducida, el vector solución, el mensaje, True y None

    # Respaldo para los casos en que se calcula RREF pero no se ajusta a los patrones de solución estándar Ax=b
    # por ejemplo, una matriz A no cuadrada donde el usuario solo quiere RREF de [A|b]
    msg = "Matriz en forma escalonada reducida (RREF) calculada." # Mensaje
    steps_ref.append(msg) # Agrega el mensaje a los pasos
    return rref_output, None, msg, True, None # Retorna la matriz en forma escalonada reducida, None, el mensaje, True y None

@router.post("/gauss_jordan_elimination", response_model=ApiResponse)
async def solve_system_gauss_jordan(payload: SystemInput) -> ApiResponse:
    steps_log = [] # Inicializa el registro de pasos
    try:
        matrix_a_orig = payload.matrix_a # Obtiene la matriz A original
        vector_b_orig = payload.vector_b # Obtiene el vector b original

        num_filas_a, num_cols_a, error_val_a = validar_matriz(matrix_a_orig, "A") # Valida la matriz A
        if error_val_a: raise ValueError(f"{error_val_a}") # Mensaje de error más simple para HTTPException
        
        num_elems_b, error_val_b = validar_vector(vector_b_orig, "b") # Valida el vector b
        if error_val_b: raise ValueError(f"{error_val_b}")

        if num_filas_a is None or num_cols_a is None or num_elems_b is None:
             raise HTTPException(status_code=500, detail="Error interno obteniendo dimensiones validadas.")

        if num_filas_a != num_elems_b:
            raise ValueError(f"El número de filas de la matriz A ({num_filas_a}) debe coincidir con el número de elementos del vector b ({num_elems_b}).")

        # Límites de dimensión (máximo 4x4 para A, por lo que aumentada es máximo 4x5)
        if num_filas_a > 4: raise ValueError(f"La matriz A está limitada a un máximo de 4 filas. Se recibió {num_filas_a}x{num_cols_a}.")
        if num_cols_a > 4: raise ValueError(f"La matriz A está limitada a un máximo de 4 columnas. Se recibió {num_filas_a}x{num_cols_a}.")

        matrix_a_frac: Matrix = [] # Inicializa la matriz A de fracciones
        for i, row_a in enumerate(matrix_a_orig): # Itera sobre las filas de la matriz A original
            current_row_frac_a = [] # Inicializa la fila actual de fracciones de A
            for j, val_a in enumerate(row_a): # Itera sobre los valores de la fila actual
                try: current_row_frac_a.append(to_fraction(val_a)) # Convierte el valor a fracción y lo agrega a la fila actual
                except ValueError as e: raise ValueError(f"Error de conversión en A[{i+1}][{j+1}]: {e}") # Lanza un error si la conversión falla
            matrix_a_frac.append(current_row_frac_a) # Agrega la fila actual a la matriz A de fracciones

        vector_b_frac: List[Fraction] = [] # Inicializa el vector b de fracciones
        for i, val_b in enumerate(vector_b_orig): # Itera sobre los valores del vector b original
            try: vector_b_frac.append(to_fraction(val_b)) # Convierte el valor a fracción y lo agrega al vector b
            except ValueError as e: raise ValueError(f"Error de conversión en b[{i+1}]: {e}") # Lanza un error si la conversión falla
        
        steps_log.append("Matriz A original:"); steps_log.extend(format_matrix_for_steps(matrix_a_frac, f"A ({num_filas_a}x{num_cols_a})")) # Agrega la matriz A original a los pasos
        steps_log.append("Vector de constantes b:"); steps_log.extend(format_matrix_for_steps([[val] for val in vector_b_frac], f"b ({num_elems_b}x1)")) # Agrega el vector b original a los pasos
        
        rref_matrix, solution_vector, message, rref_calc_ok, calc_error_detail = _gauss_jordan_elimination(
            matrix_a_frac, vector_b_frac, steps_log
        ) # Llama a la función de eliminación de Gauss-Jordan

        api_success_status = False # Valor predeterminado para ApiResponse.success
        error_for_response = calc_error_detail # Inicializa el error para la respuesta

        if rref_calc_ok: # Si el cálculo de RREF fue exitoso
            if message == "El sistema tiene una solución única.": # Si el sistema tiene una solución única
                api_success_status = True # El estado de la API es exitoso
                error_for_response = None  # No hay error
            elif message == "El sistema tiene soluciones infinitas.": # Si el sistema tiene soluciones infinitas
                api_success_status = True # La prueba espera True
                error_for_response = None # No hay error si se determinaron con éxito soluciones infinitas
            elif message == "El sistema no tiene solución (es inconsistente).": # Si el sistema no tiene solución (es inconsistente)
                api_success_status = False # La prueba espera False
                # error_for_response ya es el mensaje de inconsistencia de calc_error_detail
            elif message == "Matriz en forma escalonada reducida (RREF) calculada.": # Si la matriz en forma escalonada reducida (RREF) fue calculada
                 api_success_status = True # Para la prueba A_not_square_gj y otros casos de solo RREF
                 error_for_response = None # No hay error
            else: # Algún otro mensaje de la lógica central, o rref_calc_ok era True pero calc_error tenía un mensaje diferente
                api_success_status = False 
                if not error_for_response: error_for_response = message or "Resultado inesperado del cálculo de RREF." # Si no hay error, el error es el mensaje o "Resultado inesperado del cálculo de RREF."
        else: # rref_calc_ok es False - falló el algoritmo central
            api_success_status = False # El estado de la API es falso
            if not error_for_response: error_for_response = "Fallo interno en el cálculo de Gauss-Jordan." # Si no hay error, el error es "Fallo interno en el cálculo de Gauss-Jordan."

        response_payload = {"message": message, "solution_vector": solution_vector, "rref_matrix": rref_matrix} # Crea la carga útil de la respuesta
        return ApiResponse(success=api_success_status, result=response_payload, steps=steps_log, error=error_for_response) # Retorna la respuesta de la API

    except ValueError as e: # Atrapa los errores de validación antes de la lógica central
        raise HTTPException(status_code=400, detail=str(e)) # Lanza una excepción HTTP
    except HTTPException as e: # Vuelve a lanzar las excepciones HTTP si ocurren
        raise e # Lanza la excepción
    except Exception as e: # Captura todos los errores inesperados
        # import traceback; traceback.print_exc(); # Para la depuración del lado del servidor
        return ApiResponse(success=False, result=None, error=f"Error inesperado: {str(e)}", steps=steps_log or ["Error inesperado."]) # Retorna una respuesta de error
