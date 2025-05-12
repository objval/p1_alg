import pytest
from fastapi.testclient import TestClient
from backend.main import app # Assuming your FastAPI app instance is named 'app'

client = TestClient(app)

# Test cases for successful matrix multiplication
VALID_MULTIPLICATION_CASES = [
    (
        {"matrix_a": [[1, 2], [3, 4]], "matrix_b": [[2, 0], [1, 2]]},
        {"success": True, "result": [[4, 4], [10, 8]]}
    ),
    (
        {"matrix_a": [[1, 2, 3], [4, 5, 6]], "matrix_b": [[7, 8], [9, 10], [11, 12]]},
        {"success": True, "result": [[58, 64], [139, 154]]}
    ),
    (
        {"matrix_a": [[2]], "matrix_b": [[3]]},
        {"success": True, "result": [[6]]}
    ),
    (
        {"matrix_a": [[1, 2], [3, "1/2"]], "matrix_b": [["1/5", 0], [1, "2/3"]],},
        {"success": True, "result": [["11/5", "4/3"], ["11/10", "1/3"]]}
    ),
    (
        {"matrix_a": [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "matrix_b": [[10, 20, 30], [40, 50, 60], [70, 80, 90]]},
        {"success": True, "result": [[10, 20, 30], [40, 50, 60], [70, 80, 90]]} # Identity matrix test
    ),
    (
        {"matrix_a": [[1, 2, 3]], "matrix_b": [[4], [5], [6]]},
        {"success": True, "result": [[32]]} # Row vector * Column vector
    ),
    (
        {"matrix_a": [[1], [2], [3]], "matrix_b": [[4, 5, 6]]},
        {"success": True, "result": [[4, 5, 6], [8, 10, 12], [12, 15, 18]]} # Column vector * Row vector
    ),
]

@pytest.mark.parametrize("payload, expected_response_part", VALID_MULTIPLICATION_CASES)
def test_multiply_matrices_valid(payload, expected_response_part):
    response = client.post("/operations/multiply", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == expected_response_part["success"]
    # Compare elements as strings
    expected_result_str = [[str(el) if not isinstance(el, str) else el for el in row] for row in expected_response_part["result"]]
    assert data["result"] == expected_result_str
    assert "steps" in data
    assert len(data["steps"]) > 2 # Check for presence of steps
    # Check for matrix formatting in steps (basic check)
    assert "Matriz A ingresada:" in data["steps"]
    assert "Matriz B ingresada:" in data["steps"]
    assert "Proceso de multiplicación (A x B):" in data["steps"]
    assert any("Elemento C[" in step for step in data["steps"] if isinstance(step, str))
    assert "Matriz Resultante (C = A x B):" in data["steps"]

# Test cases for invalid matrix multiplication (dimension mismatch)
INVALID_DIMENSION_CASES = [
    (
        {"matrix_a": [[1, 2], [3, 4]], "matrix_b": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
        400,
        "Para la multiplicación, el número de columnas de la matriz A (2) debe ser igual al número de filas de la matriz B (3)."
    ),
    (
        {"matrix_a": [[1, 2, 3]], "matrix_b": [[1, 2], [3, 4]]},
        400,
        "Para la multiplicación, el número de columnas de la matriz A (3) debe ser igual al número de filas de la matriz B (2)."
    ),
    (
        {"matrix_a": [[1], [2]], "matrix_b": [[1, 2, 3]]},
        200, # This is actually a valid multiplication: 2x1 * 1x3 = 2x3
        None # No error expected for this case, will be handled by valid tests
    ),
]

@pytest.mark.parametrize("payload, expected_status_code, expected_error_detail", INVALID_DIMENSION_CASES)
def test_multiply_matrices_invalid_dimensions(payload, expected_status_code, expected_error_detail):
    # Skip the case that's actually valid and covered by successful tests
    if expected_error_detail is None and expected_status_code == 200:
        pytest.skip("Valid multiplication case, tested elsewhere.")
        return

    response = client.post("/operations/multiply", json=payload)
    assert response.status_code == expected_status_code
    if expected_error_detail:
        data = response.json()
        assert data["detail"] == expected_error_detail

# Test cases for general invalid input (empty matrix, non-numeric, etc.) - piggybacks on existing validation
GENERAL_INVALID_INPUT_CASES = [
    (
        {"matrix_a": [], "matrix_b": [[1,2]]},
        400,
        "A no puede estar vacía."
    ),
    (
        {"matrix_a": [[]], "matrix_b": [[1,2]]},
        400,
        "Las filas de a no pueden estar vacías (cero columnas)."
    ),
    (
        {"matrix_a": [[1,2]], "matrix_b": []},
        400,
        "B no puede estar vacía."
    ),
    (
        {"matrix_a": [[1,2]], "matrix_b": [[]]},
        400,
        "Las filas de b no pueden estar vacías (cero columnas)."
    ),
    (
        {"matrix_a": [[1, "abc"]], "matrix_b": [[1],[2]]},
        400,
        "Valor de entrada inválido: 'abc'. No es un número, fracción (ej: '1/2'), ni string numérico (ej: '2.5')."
    ),
    (
        {"matrix_a": [[1, 2]], "matrix_b": [[1],["1/0"]]}, # Note: matrix_b_frac creation will hit this
        400,
        "Valor inválido: '1/0'. El denominador no puede ser cero en una fracción."
    ),
    (
        {"matrix_a": [[1,2,3,4,5]], "matrix_b": [[1],[1],[1],[1],[1]]}, # Exceeds column limit for A
        400,
        "La operación está limitada a matrices de hasta 4 columnas. La matriz A tiene 5 columnas."
    ),
     (
        {"matrix_a": [[1],[1],[1],[1],[1]], "matrix_b": [[1,2,3,4]]}, # Exceeds row limit for A
        400,
        "La operación está limitada a matrices de hasta 4 filas. La matriz A tiene 5 filas."
    ),

]

@pytest.mark.parametrize("payload, expected_status_code, expected_error_detail", GENERAL_INVALID_INPUT_CASES)
def test_multiply_matrices_general_invalid_input(payload, expected_status_code, expected_error_detail):
    response = client.post("/operations/multiply", json=payload)
    assert response.status_code == expected_status_code
    data = response.json()
    assert data["detail"] == expected_error_detail


def test_multiply_detailed_steps():
    payload = {"matrix_a": [[1, "1/2"], ["1/3", 0]], "matrix_b": [[2, 1], ["1/4", "1/5"]]}
    response = client.post("/operations/multiply", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    # Compare elements as strings
    expected_result_str = [[str(el) if not isinstance(el, str) else el for el in row] for row in [["17/8", "11/10"], ["2/3", "1/3"]]]
    assert data["result"] == expected_result_str
    
    expected_steps = [
        "Matriz A ingresada:",
        "Matriz A (2x2):",
        "  |   1  1/2 |",
        "  | 1/3    0 |",
        "Matriz B ingresada:",
        "Matriz B (2x2):",
        "  |   2    1 |",
        "  | 1/4  1/5 |",
        "Proceso de multiplicación (A x B):",
        "Elemento C[1][1] = (1 * 2) + (1/2 * 1/4) = 17/8",
        "Elemento C[1][2] = (1 * 1) + (1/2 * 1/5) = 11/10",
        "Elemento C[2][1] = (1/3 * 2) + (0 * 1/4) = 2/3",
        "Elemento C[2][2] = (1/3 * 1) + (0 * 1/5) = 1/3",
        "Matriz Resultante (C = A x B):",
        "Matriz Resultante C (2x2):",
        "  | 17/8  11/10 |",
        "  |  2/3    1/3 |"
    ]
    assert data["steps"] == expected_steps 