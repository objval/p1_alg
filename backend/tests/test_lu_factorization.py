import pytest
from fastapi.testclient import TestClient
from backend.main import app # Asegúrate que la app principal de FastAPI se importa correctamente

client = TestClient(app)

# --- Casos Válidos de Descomposición LU ---
VALID_LU_CASES = [
    (
        "2x2_simple",
        {"matrix": [["2", "3"], ["1", "4"]]}, # A
        {
            "success": True,
            "result": {
                "matrix_l": [["1", "0"], ["1/2", "1"]],
                "matrix_u": [["2", "3"], ["0", "5/2"]]
            }
        }
    ),
    (
        "3x3_standard",
        {"matrix": [["2", "-1", "0"], ["-1", "2", "-1"], ["0", "-1", "2"]]}, # A
        {
            "success": True,
            "result": {
                "matrix_l": [["1", "0", "0"], ["-1/2", "1", "0"], ["0", "-2/3", "1"]],
                "matrix_u": [["2", "-1", "0"], ["0", "3/2", "-1"], ["0", "0", "4/3"]]
            }
        }
    ),
    (
        "3x3_another_example", # Example from a common source
        {"matrix": [["1", "4", "3"], ["2", "5", "4"], ["1", "-3", "-2"]]}, # A
        {
            "success": True,
            "result": {
                "matrix_l": [["1", "0", "0"], ["2", "1", "0"], ["1", "7/3", "1"]],
                "matrix_u": [["1", "4", "3"], ["0", "-3", "-2"], ["0", "0", "-1/3"]]
            }
        }
    ),
    (
        "4x4_example_no_pivoting", # Needs a matrix known to not require pivoting
        # Example: A = [[1, 2, 3, 4], [2, 5, 8, 11], [3, 8, 14, 19], [4, 11, 19, 28]]
        # L = [[1,0,0,0], [2,1,0,0], [3,2,1,0], [4,3,2,1]]
        # U = [[1,2,3,4], [0,1,2,3], [0,0,1,2], [0,0,0,1]]
        {"matrix": [["1", "2", "3", "4"], ["2", "5", "8", "11"], ["3", "8", "14", "19"], ["4", "11", "19", "28"]]}, # A
        {
            "success": True,
            "result": {
                "matrix_l": [["1","0","0","0"], ["2","1","0","0"], ["3","2","1","0"], ["4","3","1","1"]],
                "matrix_u": [["1","2","3","4"], ["0","1","2","3"], ["0","0","1","1"], ["0","0","0","2"]]
            }
        }
    ),
]

@pytest.mark.parametrize("test_id, payload, expected_response", VALID_LU_CASES)
def test_lu_factorization_valid(test_id, payload, expected_response):
    response = client.post("/operations/lu_factorization", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == expected_response["success"]
    if expected_response["success"]:
        assert data["result"]["matrix_l"] == expected_response["result"]["matrix_l"]
        assert data["result"]["matrix_u"] == expected_response["result"]["matrix_u"]
    # Se pueden añadir verificaciones de los pasos si es necesario

# --- Casos Inválidos y de Error para Descomposición LU ---
INVALID_LU_CASES = [
    (
        "non_square_matrix",
        {"matrix": [["1", "2", "3"], ["4", "5", "6"]]}, 
        400,
        "La matriz A debe ser cuadrada para la descomposición LU. Se recibió 2x3."
    ),
    (
        "exceeds_4x4_limit",
        {"matrix": [[str(i*5+j+1) for j in range(5)] for i in range(5)]}, # 5x5 matrix
        400,
        "La matriz A está limitada a dimensiones de hasta 4x4 para LU. Se recibió 5x5."
    ),
    (
        "empty_matrix",
        {"matrix": []},
        400,
        "Error en Matriz A: A no puede estar vacía."
    ),
    (
        "non_numeric_element",
        {"matrix": [["1", "x"], ["3", "4"]]}, 
        400,
        "Error de conversión de valor: Valor de entrada inválido: 'x'. No es un número, fracción (ej: '1/2'), ni string numérico (ej: '2.5')."
    ),
    (
        "zero_pivot_no_pivoting", # Doolittle sin pivoteo fallará aquí
        {"matrix": [["0", "1"], ["2", "3"]]}, 
        200, # El endpoint devuelve success:false, no una HTTPException directa para este caso de cálculo
        "Error: Pivote U(1,1) es cero. La descomposición LU (sin pivoteo) no es posible o la matriz es singular."
    ),
    (
        "another_zero_pivot_3x3",
        {"matrix": [["1", "1", "1"], ["1", "1", "2"], ["1", "2", "3"]]}, # U(2,2) se volverá cero
        200,
        "Error: Pivote U(2,2) es cero. La descomposición LU (sin pivoteo) no es posible o la matriz es singular."
    )
]

@pytest.mark.parametrize("test_id, payload, expected_status_code, expected_error_detail", INVALID_LU_CASES)
def test_lu_factorization_invalid(test_id, payload, expected_status_code, expected_error_detail):
    response = client.post("/operations/lu_factorization", json=payload)
    assert response.status_code == expected_status_code
    data = response.json()
    if expected_status_code == 400 or expected_status_code == 422:
        assert expected_error_detail in data.get("detail", str(data)) # Pydantic vs HTTPException
    elif expected_status_code == 200: # Casos donde success=False pero status=200
        assert data["success"] == False
        assert data["error"] == expected_error_detail 