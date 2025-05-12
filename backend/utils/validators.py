from typing import List, Optional, Tuple, Union
from fractions import Fraction
from backend.models import InputMatrix, Matrix # Assuming models.py is in backend/

def validar_matriz(matriz: InputMatrix, nombre_matriz: str = "La matriz", expected_rows: Optional[int] = None, expected_cols: Optional[int] = None) -> Tuple[Optional[int], Optional[int], Optional[str]]:
    if not matriz: return None, None, f"{nombre_matriz} no puede estar vacía."
    num_filas = len(matriz)
    if num_filas == 0: return None, None, f"{nombre_matriz} no puede tener cero filas."
    
    if expected_rows is not None and num_filas != expected_rows:
        return num_filas, None, f"{nombre_matriz} debe tener {expected_rows} filas, pero tiene {num_filas}."

    num_columnas_primera_fila = 0
    if matriz[0] is not None:
        try: num_columnas_primera_fila = len(matriz[0])
        except TypeError: return None, None, f"La primera fila de {nombre_matriz.lower()} debe ser una lista de elementos."
    
    if expected_cols is not None and num_columnas_primera_fila != expected_cols:
        return num_filas, num_columnas_primera_fila, f"{nombre_matriz} debe tener {expected_cols} columnas, pero tiene {num_columnas_primera_fila}."

    # Check for list of empty lists specifically for column count
    if num_columnas_primera_fila == 0 and num_filas > 0 and isinstance(matriz[0], list):
         return num_filas, 0, f"Las filas de {nombre_matriz.lower()} no pueden estar vacías (cero columnas)." # num_columnas_primera_fila is 0 here
    
    for i, fila in enumerate(matriz):
        if not isinstance(fila, list): return num_filas, None, f"Cada elemento de {nombre_matriz.lower()} debe ser una fila (lista). La fila {i+1} no es una lista."
        if not fila and num_columnas_primera_fila > 0: return num_filas, num_columnas_primera_fila, f"La fila {i+1} de {nombre_matriz.lower()} no puede ser una lista vacía si otras filas tienen elementos."
        if len(fila) != num_columnas_primera_fila: return num_filas, num_columnas_primera_fila, f"Todas las filas de {nombre_matriz.lower()} deben tener el mismo número de columnas. La fila {i+1} tiene {len(fila)} columnas, se esperaban {num_columnas_primera_fila}."
    return num_filas, num_columnas_primera_fila, None

def validar_dimensiones_para_suma_resta(matrix_a: InputMatrix, matrix_b: InputMatrix) -> Optional[str]:
    filas_a, cols_a, error_a = validar_matriz(matrix_a, "La matriz A")
    if error_a: return error_a
    filas_b, cols_b, error_b = validar_matriz(matrix_b, "La matriz B")
    if error_b: return error_b
    if filas_a != filas_b: return f"Las matrices A y B deben tener el mismo número de filas para la suma/resta. A tiene {filas_a} filas y B tiene {filas_b} filas."
    if cols_a != cols_b: return f"Las matrices A y B deben tener el mismo número de columnas para la suma/resta. A tiene {cols_a} columnas y B tiene {cols_b} columnas."
    if filas_a is not None and filas_a > 4: return f"La operación está limitada a matrices de hasta 4 filas. La matriz A tiene {filas_a} filas."
    if cols_a is not None and cols_a > 4: return f"La operación está limitada a matrices de hasta 4 columnas. La matriz A tiene {cols_a} columnas."
    return None 

def validar_dimensiones_para_multiplicacion(matrix_a: Matrix, matrix_b: Matrix) -> Tuple[bool, str]:
    """
    Valida que las dimensiones de las matrices sean compatibles para la multiplicación.
    El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.

    Args:
        matrix_a: La primera matriz.
        matrix_b: La segunda matriz.

    Returns:
        Tuple[bool, str]: (True, "") si las dimensiones son compatibles, (False, "mensaje de error") en caso contrario.
    """
    if not matrix_a or not matrix_a[0]:
        return False, "La primera matriz (A) no puede estar vacía."
    if not matrix_b or not matrix_b[0]:
        return False, "La segunda matriz (B) no puede estar vacía."

    cols_a = len(matrix_a[0])
    rows_b = len(matrix_b)

    if cols_a != rows_b:
        return False, f"Para la multiplicación, el número de columnas de la matriz A ({cols_a}) debe ser igual al número de filas de la matriz B ({rows_b})."
    return True, ""

def validar_vector(vector: List[Union[int, float, str]], nombre_vector: str = "El vector", expected_len: Optional[int] = None) -> Tuple[Optional[int], Optional[str]]:
    """
    Valida un vector (lista de elementos).

    Args:
        vector: La lista de elementos que representa el vector.
        nombre_vector: Nombre descriptivo del vector para mensajes de error.
        expected_len: Longitud esperada opcional para el vector.

    Returns:
        Tuple[Optional[int], Optional[str]]: (longitud_del_vector, None) si es válido,
                                              (None, mensaje_de_error) si es inválido.
    """
    if not isinstance(vector, list):
        return None, f"{nombre_vector} debe ser una lista."
    
    if not vector:
        return None, f"{nombre_vector} no puede estar vacío."
    
    longitud_vector = len(vector)

    if expected_len is not None and longitud_vector != expected_len:
        return longitud_vector, f"{nombre_vector} debe tener {expected_len} elementos, pero tiene {longitud_vector}."

    # No se valida el tipo de elemento aquí, eso se hace durante la conversión a Fraction en la lógica de la operación.
    # Esta función se centra en la estructura y longitud.
    
    return longitud_vector, None

# TODO: Considerar añadir validación para matrices de escalares individuales si se decide soportar (e.g., [[2]] * [[3,4]]) 