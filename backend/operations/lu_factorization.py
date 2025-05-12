from fastapi import APIRouter, HTTPException
from typing import List, Tuple
from fractions import Fraction

from backend.models import MatrixInput, ApiResponse, LUFactorizationResult, Matrix, OutputMatrix
from backend.utils.type_converters import to_fraction, format_fraction_output
from backend.utils.formatters import format_matrix_for_steps
from backend.utils.validators import validar_matriz

router = APIRouter()

def _lu_decomposition_doolittle(matrix_a_frac: Matrix, steps_ref: List[str]) -> Tuple[Matrix | None, Matrix | None, bool, str | None]:
    """
    Realiza la descomposición LU de una matriz A utilizando el método de Doolittle.
    A = LU, donde L es triangular inferior con 1s en la diagonal, y U es triangular superior.
    No implementa pivoteo.

    Args:
        matrix_a_frac: Matriz de entrada A (cuadrada) con elementos como Fraction.
        steps_ref: Lista para registrar los pasos detallados del cálculo.

    Returns:
        Tuple[Matrix | None, Matrix | None, bool, str | None]:
            - Matriz L (Matrix | None): Matriz triangular inferior L, o None si falla.
            - Matriz U (Matrix | None): Matriz triangular superior U, o None si falla.
            - success (bool): True si la descomposición fue exitosa, False en caso contrario.
            - error_message (str | None): Mensaje de error si la descomposición falla.
    """
    n = len(matrix_a_frac)
    if n == 0:
        return None, None, False, "La matriz de entrada no puede estar vacía."
    
    # Inicializar matrices L y U con ceros
    L = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    U = [[Fraction(0) for _ in range(n)] for _ in range(n)]

    steps_ref.append("Inicializando matrices L y U.")
    steps_ref.extend(format_matrix_for_steps([[format_fraction_output(el) for el in row] for row in L], "Matriz L Inicial"))
    steps_ref.extend(format_matrix_for_steps([[format_fraction_output(el) for el in row] for row in U], "Matriz U Inicial"))

    steps_ref.append("Calculando elementos de L y U:")

    for k in range(n):
        # Calcular diagonal de L (siempre 1 para Doolittle) y elementos de U en la fila k
        L[k][k] = Fraction(1)
        steps_ref.append(f"  L({k+1},{k+1}) = 1 (Diagonal de L en Doolittle)")

        steps_ref.append(f"  Calculando fila {k+1} de U:")
        for j in range(k, n): # Columnas de U
            sum_lu = Fraction(0)
            for p in range(k): # Sumatoria de L[k][p] * U[p][j]
                sum_lu += L[k][p] * U[p][j]
            
            U[k][j] = matrix_a_frac[k][j] - sum_lu
            steps_ref.append(f"    U({k+1},{j+1}) = A({k+1},{j+1}) - Σ(L({k+1},p)*U(p,{j+1})) for p=1 to {k}")
            steps_ref.append(f"             = {format_fraction_output(matrix_a_frac[k][j])} - {format_fraction_output(sum_lu)} = {format_fraction_output(U[k][j])}")

        # Verificar si U[k][k] es cero (pivote cero), lo que detendría la división para L
        if U[k][k] == 0:
            error_msg = f"Error: Pivote U({k+1},{k+1}) es cero. La descomposición LU (sin pivoteo) no es posible o la matriz es singular."
            steps_ref.append(error_msg)
            return None, None, False, error_msg
        
        # Calcular elementos de L en la columna k (debajo de la diagonal)
        if k + 1 < n: # Solo si hay filas debajo de la actual
             steps_ref.append(f"  Calculando columna {k+1} de L (debajo de la diagonal):")
        for i in range(k + 1, n): # Filas de L
            sum_lu = Fraction(0)
            for p in range(k): # Sumatoria de L[i][p] * U[p][k]
                sum_lu += L[i][p] * U[p][k]
            
            L[i][k] = (matrix_a_frac[i][k] - sum_lu) / U[k][k]
            steps_ref.append(f"    L({i+1},{k+1}) = (A({i+1},{k+1}) - Σ(L({i+1},p)*U(p,{k+1}))) / U({k+1},{k+1}) for p=1 to {k}")
            steps_ref.append(f"             = ({format_fraction_output(matrix_a_frac[i][k])} - {format_fraction_output(sum_lu)}) / {format_fraction_output(U[k][k])} = {format_fraction_output(L[i][k])}")

    steps_ref.append("Descomposición LU completada.")
    return L, U, True, None


@router.post("/lu_factorization", response_model=ApiResponse, summary="Descomposición LU de una matriz (método Doolittle sin pivoteo)")
async def lu_factorization_endpoint(data: MatrixInput):
    """
    Realiza la descomposición LU de una matriz A, de forma que A = LU.
    L es una matriz triangular inferior con unos en la diagonal.
    U es una matriz triangular superior.
    La implementación actual no utiliza pivoteo.
    """
    steps: List[str] = []

    # 1. Validar Matriz A
    rows_a, cols_a, error_msg_val = validar_matriz(data.matrix, "A")
    if error_msg_val:
        raise HTTPException(status_code=400, detail=f"Error en Matriz A: {error_msg_val}")
    
    if rows_a is None or cols_a is None: # Salvaguarda, validar_matriz debería asegurar esto
        raise HTTPException(status_code=500, detail="Error interno al obtener dimensiones de la matriz A.")

    # Validaciones específicas para LU
    if rows_a != cols_a:
        raise HTTPException(status_code=400, detail=f"La matriz A debe ser cuadrada para la descomposición LU. Se recibió {rows_a}x{cols_a}.")
    if rows_a > 4: # Mantenemos límite de 4x4
        raise HTTPException(status_code=400, detail=f"La matriz A está limitada a dimensiones de hasta 4x4 para LU. Se recibió {rows_a}x{cols_a}.")

    n = rows_a

    # 2. Conversión a Fracciones
    matrix_a_frac: Matrix = []
    try:
        for i, row_data in enumerate(data.matrix):
            if len(row_data) != n: # Redundante si validar_matriz chequea rectangularidad
                 raise ValueError(f"La fila {i+1} de la matriz A tiene {len(row_data)} elementos, se esperaban {n}.")
            matrix_a_frac.append([to_fraction(val) for val in row_data])
    except ValueError as e: # Captura errores de to_fraction
        raise HTTPException(status_code=400, detail=f"Error de conversión de valor: {str(e)}")

    steps.append("Matriz de entrada A:")
    steps.extend(format_matrix_for_steps(matrix_a_frac, f"A ({n}x{n})"))

    # 3. Descomposición LU
    matrix_l_frac, matrix_u_frac, success, error_lu = _lu_decomposition_doolittle(matrix_a_frac, steps)

    if not success or matrix_l_frac is None or matrix_u_frac is None:
        # El error_lu ya está en los steps si fue generado por _lu_decomposition_doolittle
        # Si no hay error_lu específico pero falló, usar un mensaje genérico.
        error_message = error_lu if error_lu else "No se pudo completar la descomposición LU."
        return ApiResponse(success=False, error=error_message, steps=steps, result=None)

    # 4. Formatear matrices L y U para la salida
    output_l: OutputMatrix = [[format_fraction_output(el) for el in row] for row in matrix_l_frac]
    output_u: OutputMatrix = [[format_fraction_output(el) for el in row] for row in matrix_u_frac]

    steps.append("Matriz L final:")
    steps.extend(format_matrix_for_steps(output_l, "L"))
    steps.append("Matriz U final:")
    steps.extend(format_matrix_for_steps(output_u, "U"))
    
    # Verificar A = L*U (opcional, para depuración o como paso extra)
    # Product_LU = [[sum(L[i][k] * U[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    # steps.append("Verificación (L*U):")
    # steps.extend(format_matrix_for_steps([[format_fraction_output(el) for el in row] for row in Product_LU], "L*U"))


    return ApiResponse(
        success=True,
        result=LUFactorizationResult(matrix_l=output_l, matrix_u=output_u),
        steps=steps
    ) 