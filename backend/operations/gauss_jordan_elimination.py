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
    n_rows = len(matrix_a_frac)
    if n_rows == 0:
        return None, None, "Error: Matriz A no puede ser vacía.", False, "Matriz A vacía."
    
    n_cols_a = 0
    if matrix_a_frac and matrix_a_frac[0]: # Check if the first row exists and is not empty
        n_cols_a = len(matrix_a_frac[0])
    
    if n_cols_a == 0: # Handles if matrix_a_frac was [[]] or similar
         return None, None, "Error: Matriz A no puede tener cero columnas.", False, "Matriz A sin columnas."

    augmented_matrix: Matrix = [row[:] + [vector_b_frac[i]] for i, row in enumerate(matrix_a_frac)]
    n_cols_aug = n_cols_a + 1
    
    steps_ref.append("Matriz aumentada inicial [A|b]:")
    steps_ref.extend(format_matrix_for_steps(augmented_matrix, f"Aumentada ({n_rows}x{n_cols_aug})"))

    pivot_row = 0
    for col in range(n_cols_a): 
        if pivot_row >= n_rows: break

        i_max = pivot_row
        for i in range(pivot_row + 1, n_rows):
            if abs(augmented_matrix[i][col]) > abs(augmented_matrix[i_max][col]):
                i_max = i
        
        # Using a very small number to check for effective zero for pivot
        # This tolerance might need adjustment depending on expected precision
        if abs(augmented_matrix[i_max][col]) < Fraction(1, 10**12): 
            steps_ref.append(f"  Pivote en columna {col+1} (para A({pivot_row+1},{col+1})) es cero o insignificante. Saltando esta columna.")
            continue

        if i_max != pivot_row:
            augmented_matrix[pivot_row], augmented_matrix[i_max] = augmented_matrix[i_max], augmented_matrix[pivot_row]
            steps_ref.append(f"  Intercambiando Fila {pivot_row+1} con Fila {i_max+1}.")
            steps_ref.extend(format_matrix_for_steps(augmented_matrix, "Después de intercambio"))

        pivot_element = augmented_matrix[pivot_row][col]
        if pivot_element != 1:
            steps_ref.append(f"  Normalizando Fila {pivot_row+1}: F{pivot_row+1} = F{pivot_row+1} / {format_fraction_output(pivot_element)}")
            for j in range(col, n_cols_aug):
                augmented_matrix[pivot_row][j] /= pivot_element
            steps_ref.extend(format_matrix_for_steps(augmented_matrix, "Después de normalizar"))
        
        for i in range(n_rows):
            if i != pivot_row:
                factor = augmented_matrix[i][col]
                if factor != 0:
                    steps_ref.append(f"  Eliminando en Fila {i+1}: F{i+1} = F{i+1} - ({format_fraction_output(factor)}) * F{pivot_row+1}")
                    for j in range(col, n_cols_aug):
                        augmented_matrix[i][j] -= factor * augmented_matrix[pivot_row][j]
                    steps_ref.extend(format_matrix_for_steps(augmented_matrix, f"Después de F{i+1}"))
        pivot_row += 1

    rref_output = [[format_fraction_output(el) for el in r_row] for r_row in augmented_matrix]
    steps_ref.append("Forma escalonada reducida por filas (RREF) de la matriz aumentada:")
    steps_ref.extend(format_matrix_for_steps(rref_output, f"RREF ({n_rows}x{n_cols_aug})"))
    
    rank_A = 0
    # More robust rank calculation: count non-zero rows in A-part of RREF, or number of pivot columns found
    # The variable 'pivot_row' from the loop correctly represents the rank of matrix A.
    rank_A = pivot_row

    # Check for inconsistency: 0 = k where k != 0
    for i in range(rank_A, n_rows): # Check rows that should be all zero in A-part
        if all(augmented_matrix[i][j] == 0 for j in range(n_cols_a)) and augmented_matrix[i][n_cols_a] != 0:
            msg = "El sistema no tiene solución (es inconsistente)."
            err_detail = msg
            steps_ref.append(f"  Fila {i+1} de RREF ({rref_output[i]}) indica inconsistencia (0 = {rref_output[i][n_cols_a]}).")
            steps_ref.append(msg)
            return rref_output, None, msg, True, err_detail

    # Check for infinite solutions: rank_A < number of variables (n_cols_a)
    if rank_A < n_cols_a:
        msg = "El sistema tiene soluciones infinitas."
        steps_ref.append(f"  Hay {rank_A} pivotes (rango de A) y {n_cols_a} variables. Como ({rank_A} < {n_cols_a}) y el sistema es consistente.")
        steps_ref.append(msg)
        return rref_output, None, msg, True, None # No specific error for API, message in result covers it

    # Check for unique solution: rank_A == number of variables
    if rank_A == n_cols_a:
        # This implies rank_A is also <= n_rows. If system is consistent.
        solution_vector_frac = [augmented_matrix[i][n_cols_a] for i in range(n_cols_a)] # Assumes n_cols_a <= n_rows after RREF
        output_solution_list_str = [format_fraction_output(val) for val in solution_vector_frac]
        msg = "El sistema tiene una solución única."
        steps_ref.append(msg)
        steps_ref.append("Vector solución x:")
        solution_for_steps = [[val] for val in output_solution_list_str]
        steps_ref.extend(format_matrix_for_steps(solution_for_steps, f"x ({n_cols_a}x1)"))
        return rref_output, output_solution_list_str, msg, True, None

    # Fallback for cases where RREF is computed but doesn't fit standard Ax=b solution patterns
    # e.g. a non-square matrix A where user just wants RREF of [A|b]
    msg = "Matriz en forma escalonada reducida (RREF) calculada."
    steps_ref.append(msg)
    return rref_output, None, msg, True, None

@router.post("/gauss_jordan_elimination", response_model=ApiResponse)
async def solve_system_gauss_jordan(payload: SystemInput) -> ApiResponse:
    steps_log = []
    try:
        matrix_a_orig = payload.matrix_a
        vector_b_orig = payload.vector_b

        num_filas_a, num_cols_a, error_val_a = validar_matriz(matrix_a_orig, "A")
        if error_val_a: raise ValueError(f"{error_val_a}") # Simpler error message for HTTPException
        
        num_elems_b, error_val_b = validar_vector(vector_b_orig, "b")
        if error_val_b: raise ValueError(f"{error_val_b}")

        if num_filas_a is None or num_cols_a is None or num_elems_b is None:
             raise HTTPException(status_code=500, detail="Error interno obteniendo dimensiones validadas.")

        if num_filas_a != num_elems_b:
            raise ValueError(f"El número de filas de la matriz A ({num_filas_a}) debe coincidir con el número de elementos del vector b ({num_elems_b}).")

        # Dimension limits (max 4x4 for A, so augmented is max 4x5)
        if num_filas_a > 4: raise ValueError(f"La matriz A está limitada a un máximo de 4 filas. Se recibió {num_filas_a}x{num_cols_a}.")
        if num_cols_a > 4: raise ValueError(f"La matriz A está limitada a un máximo de 4 columnas. Se recibió {num_filas_a}x{num_cols_a}.")

        matrix_a_frac: Matrix = []
        for i, row_a in enumerate(matrix_a_orig):
            current_row_frac_a = []
            for j, val_a in enumerate(row_a):
                try: current_row_frac_a.append(to_fraction(val_a))
                except ValueError as e: raise ValueError(f"Error de conversión en A[{i+1}][{j+1}]: {e}")
            matrix_a_frac.append(current_row_frac_a)

        vector_b_frac: List[Fraction] = []
        for i, val_b in enumerate(vector_b_orig):
            try: vector_b_frac.append(to_fraction(val_b))
            except ValueError as e: raise ValueError(f"Error de conversión en b[{i+1}]: {e}")
        
        steps_log.append("Matriz A original:"); steps_log.extend(format_matrix_for_steps(matrix_a_frac, f"A ({num_filas_a}x{num_cols_a})"))
        steps_log.append("Vector de constantes b:"); steps_log.extend(format_matrix_for_steps([[val] for val in vector_b_frac], f"b ({num_elems_b}x1)"))
        
        rref_matrix, solution_vector, message, rref_calc_ok, calc_error_detail = _gauss_jordan_elimination(
            matrix_a_frac, vector_b_frac, steps_log
        )

        api_success_status = False # Default for ApiResponse.success
        error_for_response = calc_error_detail

        if rref_calc_ok:
            if message == "El sistema tiene una solución única.":
                api_success_status = True
                error_for_response = None 
            elif message == "El sistema tiene soluciones infinitas.":
                api_success_status = True # Test expects True
                error_for_response = None # No error if successfully determined infinite solutions
            elif message == "El sistema no tiene solución (es inconsistente).":
                api_success_status = False # Test expects False
                # error_for_response is already the inconsistency message from calc_error_detail
            elif message == "Matriz en forma escalonada reducida (RREF) calculada.":
                 api_success_status = True # For A_not_square_gj test and other RREF-only cases
                 error_for_response = None
            else: # Some other message from core logic, or rref_calc_ok was True but calc_error had a different message
                api_success_status = False 
                if not error_for_response: error_for_response = message or "Resultado inesperado del cálculo de RREF."
        else: # rref_calc_ok is False - core algorithm failed
            api_success_status = False
            if not error_for_response: error_for_response = "Fallo interno en el cálculo de Gauss-Jordan."

        response_payload = {"message": message, "solution_vector": solution_vector, "rref_matrix": rref_matrix}
        return ApiResponse(success=api_success_status, result=response_payload, steps=steps_log, error=error_for_response)

    except ValueError as e: # Catches validation errors before core logic
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e: # Re-raise HTTPExceptions if they occur
        raise e
    except Exception as e: # Catch-all for truly unexpected errors
        # import traceback; traceback.print_exc(); # For server-side debugging
        return ApiResponse(success=False, result=None, error=f"Error inesperado: {str(e)}", steps=steps_log or ["Error inesperado."])
