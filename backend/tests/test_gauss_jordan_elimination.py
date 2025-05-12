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

# --- Test Cases for Gauss-Jordan Elimination ---

# Renamed from VALID_SYSTEM_CASES_GJ for clarity
UNIQUE_SOLUTION_CASES_GJ = [
    (
        "2x2_unique_integers_gj",
        {"matrix_a": [[2, 1], [1, 3]], "vector_b": [5, 5]},
        {"success": True, "result": {"message": "El sistema tiene una solución única.", "solution_vector": ["2", "1"], "rref_matrix": [["1", "0", "2"], ["0", "1", "1"]]}}
    ),
    (
        "3x3_unique_integers_example_gj",
        {"matrix_a": [[1, 1, 1], [0, 2, 5], [2, 5, -1]], "vector_b": [6, -4, 27]},
        {"success": True, "result": {"message": "El sistema tiene una solución única.", "solution_vector": ["5", "3", "-2"], "rref_matrix": [["1", "0", "0", "5"], ["0", "1", "0", "3"], ["0", "0", "1", "-2"]]}}
    ),
    (
        "3x3_sotelo_class_gj",
        {"matrix_a": [[2, -1, 3], [1, 1, 1], [1, -1, 1]], "vector_b": [9, 6, 2]},
        {"success": True, "result": {"message": "El sistema tiene una solución única.", "solution_vector": ["1", "2", "3"], "rref_matrix": [["1", "0", "0", "1"], ["0", "1", "0", "2"], ["0", "0", "1", "3"]]}}
    ),
    (
        "4x4_unique_solution_gj",
        {"matrix_a": [
            [1, 1, 1, 1],
            [1, 2, 1, 1],
            [1, 1, 2, 1],
            [1, 1, 1, 2]
        ], "vector_b": [10, 12, 13, 14]},
        {"success": True, "result": {"message": "El sistema tiene una solución única.", "solution_vector": ["1", "2", "3", "4"],
                                     "rref_matrix": [
                                         ["1", "0", "0", "0", "1"],
                                         ["0", "1", "0", "0", "2"],
                                         ["0", "0", "1", "0", "3"],
                                         ["0", "0", "0", "1", "4"]
                                     ]}}
    ),
]

NO_SOLUTION_CASES_GJ = [
    (
        "2x2_inconsistent_gj",
        {"matrix_a": [[1, 1], [1, 1]], "vector_b": [2, 3]},
        {"success": False, "result": None, "error": "El sistema no tiene solución (es inconsistente).", "rref_matrix": [["1", "1", "2"],["0", "0", "1"]]}
    ),
    (
        "3x3_inconsistent_gj",
        {"matrix_a": [[1, 1, 1], [0, 1, 1], [0, 0, 0]], "vector_b": [1, 2, 3]},
        {"success": False, "result": None, "error": "El sistema no tiene solución (es inconsistente).", "rref_matrix": [['1', '0', '0', '-1'], ['0', '1', '1', '2'], ['0', '0', '0', '3']]}
    ),
    (
        "3x3_inconsistent_zero_row_A_nonzero_b_gj",
        {"matrix_a": [[1, 2, 3], [2, 4, 6], [1, 1, 1]], "vector_b": [1, 3, 2]},
        {"success": False, "result": None, "error": "El sistema no tiene solución (es inconsistente).", "rref_matrix": [['1', '0', '-1', '5/2'], ['0', '1', '2', '-1/2'], ['0', '0', '0', '-1/2']]}
    ),
    (
        "2x3_inconsistent_gj_RREF_provided",
        {"matrix_a": [[1, 1, 0], [1, 1, 0]], "vector_b": [1, 2]},
        {"success": False, "result": None, "error": "El sistema no tiene solución (es inconsistente).", "rref_matrix": [['1', '1', '0', '1'], ['0', '0', '0', '1']]}
    )
]

INFINITE_SOLUTIONS_CASES_GJ = [
     (
        "2x2_dependent_equations_gj",
        {"matrix_a": [[1, 1], [2, 2]], "vector_b": [2, 4]},
        {"success": True, "result": {"message": "El sistema tiene soluciones infinitas.", "solution_vector": None, "rref_matrix": [["1", "1", "2"],["0", "0", "0"]]}}
    ),
    (
        "3x3_one_free_variable_gj",
        {"matrix_a": [[1, 1, 1], [0, 1, 2], [0, 0, 0]], "vector_b": [6, 5, 0]},
        {"success": True, "result": {"message": "El sistema tiene soluciones infinitas.", "solution_vector": None, "rref_matrix": [["1", "0", "-1", "1"],["0", "1", "2", "5"],["0", "0", "0", "0"]]}}
    ),
    (
        "3x3_two_free_variables_gj",
        {"matrix_a": [[1, 1, 1], [0, 0, 0], [0, 0, 0]], "vector_b": [1, 0, 0]},
        {"success": True, "result": {"message": "El sistema tiene soluciones infinitas.", "solution_vector": None, "rref_matrix": [["1", "1", "1", "1"],["0", "0", "0", "0"],["0", "0", "0", "0"]]}}
    )
]

INVALID_INPUT_CASES_GJ = [
    (
        "A_not_square_gj_2x3_A_RREF_calc", # A is 2x3, b is 2x1. Augmented matrix is 2x4.
        {"matrix_a": [[1, 2, 3], [4, 5, 6]], "vector_b": [1,2]},
        200, # RREF can be computed
        # Rank is 2, num_vars (cols_A) is 3. Rank < num_vars => Infinite solutions.
        {"success": True, "result": {"message": "El sistema tiene soluciones infinitas.", "rref_matrix": [['1', '0', '-1', '-1/3'], ['0', '1', '2', '2/3']], "solution_vector": None}, "error": None}
    ),
    (
        "A_not_square_gj_2x1_A_unique_actually", # A is 2x1, b is 2x1. System: 1x=3, 2x=6.
        {"matrix_a": [[1],[2]], "vector_b": [3,6]},
        200, # RREF of [1|3],[2|6] -> [1|3],[0|0]
        # Rank is 1, num_vars (cols_A) is 1. Rank == num_vars => Unique solution.
        {"success": True, "result": {"message": "El sistema tiene una solución única.", "rref_matrix": [['1', '3'], ['0', '0']], "solution_vector": ['3']}, "error": None}
    ),
    (
        "empty_A_gj",
        {"matrix_a": [], "vector_b": []},
        400,
        "A no puede estar vacía."
    ),
    (
        "A_invalid_char_gj",
        {"matrix_a": [['x']], "vector_b": [1]},
        400,
        "Error de conversión en A[1][1]: Valor de entrada inválido: \'x\'"
    ),
    (
        "b_invalid_char_gj",
        {"matrix_a": [[1]], "vector_b": ['y']},
        400,
        "Error de conversión en b[1]: Valor de entrada inválido: \'y\'"
    ),
    (
        "A_too_large_rows_gj",
        {"matrix_a": [[1,1],[1,1],[1,1],[1,1],[1,1]], "vector_b": [1,1,1,1,1]},
        400,
        "La matriz A está limitada a un máximo de 4 filas. Se recibió 5x2."
    ),
    (
        "A_too_large_cols_gj",
        {"matrix_a": [[1,1,1,1,1],[1,1,1,1,1]], "vector_b": [1,1]},
        400,
        "La matriz A está limitada a un máximo de 4 columnas. Se recibió 2x5."
    ),
    (
        "A_b_dimension_mismatch_gj", # This is the same as A_b_rows_mismatch_gj
        {"matrix_a": [[1,2], [3,4]], "vector_b": [1,2,3]},
        400,
        "El número de filas de la matriz A (2) debe coincidir con el número de elementos del vector b (3)."
    ),
    (
        "A_jagged_matrix_gj",
        {"matrix_a": [[1, 2], [3]], "vector_b": [1,1]},
        400,
        "Todas las filas de a deben tener el mismo número de columnas. La fila 2 tiene 1 columnas, se esperaban 2."
    ),
    (
        "b_not_vector_gj",
        {"matrix_a": [[1]], "vector_b": [[1]]}, # vector_b is a matrix
        422, # Pydantic will catch this as unprocessable entity before our custom validator
        "" # We won't check the exact detail for Pydantic's 422 error
    )
]


@pytest.mark.parametrize("test_name, payload, expected_response_part", UNIQUE_SOLUTION_CASES_GJ)
def test_solve_system_gauss_jordan_unique_solution(client, test_name, payload, expected_response_part):
    response = client.post("/operations/gauss_jordan_elimination", json=payload)
    data = response.json()
    assert response.status_code == 200, f"Test: {test_name} - Expected 200, got {response.status_code}. Response: {data}"
    assert data["success"] == expected_response_part["success"], f"Test: {test_name} - Success mismatch. Response: {data}"
    assert data["result"]["message"] == expected_response_part["result"]["message"], f"Test: {test_name} - Result message mismatch. Response: {data}"
    if "solution_vector" in expected_response_part["result"]:
        assert data["result"]["solution_vector"] == expected_response_part["result"]["solution_vector"], f"Test: {test_name} - Solution vector mismatch. Response: {data}"
    if "rref_matrix" in expected_response_part["result"]:
        assert data["result"]["rref_matrix"] == expected_response_part["result"]["rref_matrix"], f"Test: {test_name} - RREF matrix mismatch. Response: {data}"
    assert "steps" in data and isinstance(data["steps"], list) and len(data["steps"]) > 0, f"Test: {test_name} - Steps missing or invalid. Response: {data}"

@pytest.mark.parametrize("test_name, payload, expected_response_part", NO_SOLUTION_CASES_GJ)
def test_solve_system_gauss_jordan_no_solution(client, test_name, payload, expected_response_part):
    response = client.post("/operations/gauss_jordan_elimination", json=payload)
    data = response.json()
    assert response.status_code == 200, f"Test: {test_name} - Expected 200, got {response.status_code}. Response: {data}"
    assert data["success"] == expected_response_part["success"], f"Test: {test_name} - Success mismatch. Response: {data}"
    assert data.get("error") == expected_response_part.get("error"), f"Test: {test_name} - Error field mismatch. Response: {data}"
    if "rref_matrix" in expected_response_part and expected_response_part["rref_matrix"] is not None:
        assert data["result"] is not None, f"Test: {test_name} - Result field is None but RREF matrix expected. Response: {data}"
        assert data["result"]["rref_matrix"] == expected_response_part["rref_matrix"], f"Test: {test_name} - RREF matrix mismatch for no solution. Response: {data}"
    assert "steps" in data and isinstance(data["steps"], list) and len(data["steps"]) > 0, f"Test: {test_name} - Steps missing or invalid. Response: {data}"


@pytest.mark.parametrize("test_name, payload, expected_response_part", INFINITE_SOLUTIONS_CASES_GJ)
def test_solve_system_gauss_jordan_infinite_solutions(client, test_name, payload, expected_response_part):
    response = client.post("/operations/gauss_jordan_elimination", json=payload)
    data = response.json()
    assert response.status_code == 200, f"Test: {test_name} - Expected 200, got {response.status_code}. Response: {data}"
    assert data["success"] == expected_response_part["success"], f"Test: {test_name} - Success mismatch. Response: {data}"
    assert data["result"]["message"] == expected_response_part["result"]["message"], f"Test: {test_name} - Result message mismatch. Response: {data}"
    if "solution_vector" in expected_response_part["result"]: # Should be None for infinite
        assert data["result"]["solution_vector"] == expected_response_part["result"]["solution_vector"], f"Test: {test_name} - Solution vector mismatch. Response: {data}"
    if "rref_matrix" in expected_response_part["result"]:
         assert data["result"]["rref_matrix"] == expected_response_part["result"]["rref_matrix"], f"Test: {test_name} - RREF matrix mismatch for infinite solutions. Response: {data}"
    # For infinite solutions, error field should be None if calculation is successful
    assert data.get("error") == expected_response_part.get("error"), f"Test: {test_name} - Error field mismatch. Expected: {expected_response_part.get('error')}, Got: {data.get('error')}"
    assert "steps" in data and isinstance(data["steps"], list) and len(data["steps"]) > 0, f"Test: {test_name} - Steps missing or invalid. Response: {data}"


@pytest.mark.parametrize("test_name, payload, expected_status_code, expected_detail_or_response", INVALID_INPUT_CASES_GJ)
def test_solve_system_gauss_jordan_invalid_input(client, test_name, payload, expected_status_code, expected_detail_or_response):
    response = client.post("/operations/gauss_jordan_elimination", json=payload)
    data = response.json()
    assert response.status_code == expected_status_code, f"Test: {test_name} - Expected {expected_status_code}, got {response.status_code}. Response: {response.text}"

    if expected_status_code == 400:
        assert "detail" in data, f"Test: {test_name} - 'detail' field missing in error response. Response: {data}"
        error_detail_str = str(data["detail"])
        assert expected_detail_or_response in error_detail_str, f"Test: {test_name} - Expected error segment '{expected_detail_or_response}' not in '{error_detail_str}'. Response: {data}"
    elif expected_status_code == 200:
        assert data["success"] == expected_detail_or_response["success"], f"Test: {test_name} - Success mismatch. Expected {expected_detail_or_response['success']}, got {data['success']}. Response: {data}"
        assert data["result"]["message"] == expected_detail_or_response["result"]["message"], f"Test: {test_name} - Result message mismatch. Response: {data}"
        if "rref_matrix" in expected_detail_or_response["result"]:
             assert data["result"]["rref_matrix"] == expected_detail_or_response["result"]["rref_matrix"], f"Test: {test_name} - RREF matrix mismatch. Response: {data}"
        if "solution_vector" in expected_detail_or_response["result"]: # Should be None for these cases
             assert data["result"]["solution_vector"] == expected_detail_or_response["result"]["solution_vector"], f"Test: {test_name} - Solution vector mismatch. Response: {data}"
        # Error field should match, typically None for these 200 OK cases
        assert data.get("error") == expected_detail_or_response.get("error"), f"Test: {test_name} - Error field mismatch. Expected: {expected_detail_or_response.get('error')}, Got: {data.get('error')}"
        assert "steps" in data and isinstance(data["steps"], list) and len(data["steps"]) > 0, f"Test: {test_name} - Steps missing or invalid. Response: {data}"
    elif expected_status_code == 422: # Added condition for Pydantic validation errors
        assert "detail" in data, f"Test: {test_name} - 'detail' field missing for 422 error. Response: {data}"
        # For 422, we are generally just checking the status code, not the specific Pydantic error structure.
        # If a specific message part was crucial, expected_detail_or_response could be used.
        pass # Test passes if status is 422 and detail is present
