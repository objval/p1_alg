import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ensure the main app can be imported
try:
    from main import app
except ImportError as e:
    print(f"Error importing main app: {e}")
    # Fallback for local testing if main.py is in the parent directory of backend
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from main import app

# Test client fixture
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# --- Test Cases for Gaussian Elimination (Solve System Ax=b) ---

VALID_SYSTEM_CASES = [
    (
        "2x2_unique_integers",
        {"matrix_a": [[2, 1], [1, 3]], "vector_b": [5, 5]},
        {"success": True, "result": {"message": "El sistema tiene una solución única.", "solution_vector": ["2", "1"]}}
    ),
    (
        "3x3_unique_integers_example",
        # System:
        # x + y + z = 6
        #   2y + 5z = -4
        # 2x + 5y - z = 27
        # Solution: x=23/3, y=-23/3, z=4/3
        {"matrix_a": [[1, 1, 1], [0, 2, 5], [2, 5, -1]], "vector_b": [6, -4, 27]},
        {"success": True, "result": {"message": "El sistema tiene una solución única.", "solution_vector": ["5", "3", "-2"]}}
    ),
    (
        "2x2_unique_with_zero_solution_element",
        {"matrix_a": [[1, 1], [1, 0]], "vector_b": [3, 1]}, # x=1, y=2
        {"success": True, "result": {"solution_vector": ["1", "2"], "message": "El sistema tiene una solución única."}}
    ),
    (
        "3x3_example_sotelo_class", # From a class example
        # 2x - y + 3z = 9
        #  x + y +  z = 6
        #  x - y +  z = 2
        # Sol: x=1, y=2, z=3
        {"matrix_a": [[2, -1, 3], [1, 1, 1], [1, -1, 1]], "vector_b": [9, 6, 2]},
        {"success": True, "result": {"solution_vector": ["1", "2", "3"], "message": "El sistema tiene una solución única."}}
    ),
    # TODO: Add a 4x4 unique solution case
]

NO_SOLUTION_CASES = [
    (
        "2x2_inconsistent",
        {"matrix_a": [[1, 1], [1, 1]], "vector_b": [2, 3]},
        {"success": True, "result": {"message": "El sistema no tiene solución (es inconsistente)."}, "error": "El sistema no tiene solución (es inconsistente)."}
    ),
    (
        "3x3_inconsistent_zero_row_A_nonzero_b",
        # R2 = 2*R1, but b2 != 2*b1  (2*1 != 3)
        {"matrix_a": [[1, 2, 3], [2, 4, 6], [1, 1, 1]], "vector_b": [1, 3, 2]},
        {"success": True, "result": {"message": "El sistema no tiene solución (es inconsistente)."}, "error": "El sistema no tiene solución (es inconsistente)."}
    ),
]

INFINITE_SOLUTIONS_CASES = [
     (
        "2x2_dependent_equations",
        {"matrix_a": [[1, 1], [2, 2]], "vector_b": [2, 4]}, # R2 = 2*R1, b2 = 2*b1
        {"success": True, "result": {"message": "El sistema tiene soluciones infinitas."}}
    ),
    (
        "3x3_one_free_variable_row_of_zeros", # e.g. z is free
        {"matrix_a": [[1, 1, 1], [0, 1, 2], [0, 0, 0]], "vector_b": [6, 5, 0]},
        {"success": True, "result": {"message": "El sistema tiene soluciones infinitas."}}
    ),
    (
        "3x3_dependent_rows_cols_consistent",
        # R3 = 2*R2 - R1, and b3 = 2*b2 - b1 (3 = 2*2 - 1). Consistent, infinite solutions.
        {"matrix_a": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "vector_b": [1, 2, 3]},
        {"success": True, "result": {"message": "El sistema tiene soluciones infinitas."}}
    ),
]

INVALID_INPUT_CASES_GAUSSIAN = [
    (
        "A_not_square_when_cols_gt_rows",
        {"matrix_a": [[1, 2, 3], [4, 5, 6]], "vector_b": [1, 2]},
        400,
        "La matriz de coeficientes A debe ser cuadrada para este método simplificado de solución única."
    ),
    (
        "A_not_square_when_rows_gt_cols",
        {"matrix_a": [[1, 2], [3, 4], [5, 6]], "vector_b": [1, 2, 3]},
        400,
        "La matriz de coeficientes A debe ser cuadrada para este método simplificado de solución única."
    ),
    (
        "A_b_rows_mismatch",
        {"matrix_a": [[1,2], [3,4]], "vector_b": [1,2,3]},
        400,
        "El número de filas de la matriz A (2) debe coincidir con el número de elementos del vector b (3)."
    ),
    (
        "empty_A",
        {"matrix_a": [], "vector_b": []},
        400,
        "Error en Matriz A: A no puede estar vacía."
    ),
    (
        "empty_b_with_A",
        {"matrix_a": [[1]], "vector_b": []},
        400,
        "Error en Vector b: El vector b no puede estar vacío."
    ),
    (
        "A_ragged",
        {"matrix_a": [[1, 2], [3]], "vector_b": [1,2]},
        400,
        "Error en Matriz A: Todas las filas de a deben tener el mismo número de columnas. La fila 2 tiene 1 columnas, se esperaban 2."
    ),
    (
        "A_invalid_char",
        {"matrix_a": [['x']], "vector_b": [1]},
        400,
        "Error de conversión de valor: Valor de entrada inválido: 'x'."
    ),
    (
        "b_invalid_char",
        {"matrix_a": [[1]], "vector_b": ['y']},
        400,
        "Error de conversión de valor: Valor de entrada inválido: 'y'."
    ),
    (
        "A_too_large_rows",
        {"matrix_a": [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]], "vector_b": [1,1,1,1,1]},
        400,
        "La matriz A está limitada a dimensiones de hasta 4x4. Se recibió 5x5."
    ),
    (
        "A_too_large_cols",
        {"matrix_a": [[1,1,1,1,1]], "vector_b": [1]},
        400,
        "La matriz A está limitada a dimensiones de hasta 4x4. Se recibió 1x5."
    )
    # Note: Test cases for b_is_empty_list_explicit (duplicate of empty_b_with_A)
    # and other conceptual b validation states that are either covered by Pydantic/to_fraction
    # or are valid inputs were removed for clarity and to avoid test redundancy.
]

# Filter out placeholder/comment entries and invalid test structures
INVALID_INPUT_CASES_GAUSSIAN = [
    case for case in INVALID_INPUT_CASES_GAUSSIAN
    if isinstance(case, tuple) and len(case) == 4 and case[0] not in [
        "b_is_not_list_of_lists_implicitly",
        "b_is_empty_list_explicit",
        "b_has_wrong_col_count_if_it_were_matrix"
    ]
]

@pytest.mark.parametrize("test_name, payload, expected_response_part", VALID_SYSTEM_CASES)
def test_solve_system_gaussian_valid(client, test_name, payload, expected_response_part):
    response = client.post("/operations/solve_system_gaussian", json=payload)
    data = response.json()
    assert response.status_code == 200, f"Test: {test_name} - Expected 200, got {response.status_code}. Response: {data}"
    assert data["success"] == expected_response_part["success"], f"Test: {test_name} - Success mismatch. Response: {data}"
    assert data["result"] == expected_response_part["result"], f"Test: {test_name} - Result mismatch. Response: {data}"
    assert "steps" in data and isinstance(data["steps"], list) and len(data["steps"]) > 0, f"Test: {test_name} - Steps missing or invalid. Response: {data}"

@pytest.mark.parametrize("test_name, payload, expected_response_part", NO_SOLUTION_CASES)
def test_solve_system_gaussian_no_solution(client, test_name, payload, expected_response_part):
    response = client.post("/operations/solve_system_gaussian", json=payload)
    data = response.json()
    assert response.status_code == 200, f"Test: {test_name} - Expected 200, got {response.status_code}. Response: {data}"
    assert data["success"] == expected_response_part["success"], f"Test: {test_name} - Success mismatch. Response: {data}"
    # For no solution, the primary 'message' is in result.message
    assert data["result"]["message"] == expected_response_part["result"]["message"], f"Test: {test_name} - Result message mismatch. Response: {data}"
    assert data.get("error") == expected_response_part.get("error"), f"Test: {test_name} - Error field mismatch. Response: {data}"
    assert "steps" in data and isinstance(data["steps"], list) and len(data["steps"]) > 0, f"Test: {test_name} - Steps missing or invalid. Response: {data}"

@pytest.mark.parametrize("test_name, payload, expected_response_part", INFINITE_SOLUTIONS_CASES)
def test_solve_system_gaussian_infinite_solutions(client, test_name, payload, expected_response_part):
    response = client.post("/operations/solve_system_gaussian", json=payload)
    data = response.json()
    assert response.status_code == 200, f"Test: {test_name} - Expected 200, got {response.status_code}. Response: {data}"
    assert data["success"] == expected_response_part["success"], f"Test: {test_name} - Success mismatch. Response: {data}"
    assert data["result"]["message"] == expected_response_part["result"]["message"], f"Test: {test_name} - Result message mismatch. Response: {data}"
    assert data.get("error") is None, f"Test: {test_name} - Error field should be None for infinite solutions. Response: {data}"
    assert "steps" in data and isinstance(data["steps"], list) and len(data["steps"]) > 0, f"Test: {test_name} - Steps missing or invalid. Response: {data}"

@pytest.mark.parametrize("test_name, payload, expected_status_code, expected_error_detail_segment", INVALID_INPUT_CASES_GAUSSIAN)
def test_solve_system_gaussian_invalid_input(client, test_name, payload, expected_status_code, expected_error_detail_segment):
    response = client.post("/operations/solve_system_gaussian", json=payload)
    assert response.status_code == expected_status_code, f"Test: {test_name} - Expected {expected_status_code}, got {response.status_code}. Response: {response.text}"
    if expected_status_code == 400: # HTTPExceptions from FastAPI/Pydantic
        data = response.json()
        assert "detail" in data, f"Test: {test_name} - 'detail' field missing in error response. Response: {data}"
        error_detail_str = str(data["detail"])
        assert expected_error_detail_segment in error_detail_str, f"Test: {test_name} - Expected error segment '{expected_error_detail_segment}' not in '{error_detail_str}'. Response: {data}"
