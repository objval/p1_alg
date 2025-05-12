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

# --- Test Cases for Matrix Inverse ---

VALID_INVERSE_CASES = [
    (
        "2x2_identity",
        {"matrix": [[1, 0], [0, 1]]},
        {"success": True, "result": [[1, 0], [0, 1]], "error": None}
    ),
    (
        "2x2_simple_integers",
        {"matrix": [[4, 7], [2, 6]]},
        # Det = 24 - 14 = 10. Inv = 1/10 * [[6, -7], [-2, 4]]
        {"success": True, "result": [["3/5", "-7/10"], ["-1/5", "2/5"]], "error": None}
    ),
    (
        "2x2_with_fractions_input",
        {"matrix": [["1/2", "1/3"], ["1/4", "1/5"]]},
        # Det = (1/2)*(1/5) - (1/3)*(1/4) = 1/10 - 1/12 = (6-5)/60 = 1/60
        # Inv = 60 * [[1/5, -1/3], [-1/4, 1/2]]
        {"success": True, "result": [[12, -20], [-15, 30]], "error": None}
    ),
    (
        "2x2_results_in_integers",
        {"matrix": [[3, -2], [1, -1]]},
        # Det = -3 - (-2) = -1. Inv = -1 * [[-1, 2], [-1, 3]]
        {"success": True, "result": [[1, -2], [1, -3]], "error": None}
    ),
    (
        "3x3_simple_case_det_1",
        {"matrix": [[1, 2, 3], [0, 1, 4], [5, 6, 0]]},
        # Det = 1. Inverse from manual calculation:
        # Adj = [[-24, 20, -5], [18, -15, 4], [5, -4, 1]]^T
        # Inv = [[-24, 18, 5], [20, -15, -4], [-5, 4, 1]]
        {"success": True, "result": [[-24, 18, 5], [20, -15, -4], [-5, 4, 1]], "error": None}
    ),
    (
        "3x3_identity",
        {"matrix": [[1,0,0],[0,1,0],[0,0,1]]},
        {"success": True, "result": [[1,0,0],[0,1,0],[0,0,1]], "error": None}
    ),
     (
        "3x3_diagonal",
        {"matrix": [[2,0,0],[0,4,0],[0,0,5]]},
        {"success": True, "result": [["1/2",0,0],[0,"1/4",0],[0,0,"1/5"]], "error": None}
    ),
    (
        "4x4_identity",
        {"matrix": [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]},
        {"success": True, "result": [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], "error": None}
    ),
    (
        "4x4_diagonal",
        {"matrix": [[2,0,0,0],[0,1,0,0],[0,0,4,0],[0,0,0,5]]},
        {"success": True, "result": [["1/2",0,0,0],[0,1,0,0],[0,0,"1/4",0],[0,0,0,"1/5"]], "error": None}
    ),
    # (
    #     "4x4_example_from_numpy", # Verified with numpy.linalg.inv
    #     {"matrix": [[1, 2, 3, 4], [2, 1, 4, 3], [3, 4, 1, 2], [4, 3, 2, 1]]},
    #     # Determinant is -20 - This comment is now believed to be incorrect.
    #     # The matrix is treated as singular by Gauss-Jordan with exact fractions.
    #     {"success": True, "result": [
    #         ["-3/20", "7/20", "7/20", "-1/4"],
    #         ["7/20", "-3/20", "-1/4", "7/20"],
    #         ["7/20", "-1/4", "-3/20", "7/20"],
    #         ["-1/4", "7/20", "7/20", "-3/20"]
    #     ], "error": None}
    # )
]

SINGULAR_MATRIX_CASES = [
    (
        "2x2_determinant_zero",
        {"matrix": [[1, 2], [2, 4]]},
        {"success": False, "result": None, "error": "La matriz no es invertible (singular). Los pasos detallan el problema."}
    ),
    (
        "2x2_all_zeros",
        {"matrix": [[0,0],[0,0]]},
        {"success": False, "result": None, "error": "La matriz no es invertible (singular). Los pasos detallan el problema."}
    ),
    (
        "3x3_determinant_zero_linear_dependent_rows",
        {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}, # R3 = 2*R2 - R1
        {"success": False, "result": None, "error": "La matriz no es invertible (singular). Los pasos detallan el problema."}
    ),
    (
        "3x3_zero_row",
        {"matrix": [[1,2,3],[0,0,0],[4,5,6]]},
        {"success": False, "result": None, "error": "La matriz no es invertible (singular). Los pasos detallan el problema."}
    ),
    (
        "4x4_determinant_zero", # Example: two identical rows
        {"matrix": [[1,2,3,4],[5,6,7,8],[1,2,3,4],[9,10,11,12]]},
        {"success": False, "result": None, "error": "La matriz no es invertible (singular). Los pasos detallan el problema."}
    ),
    (
        "4x4_example_from_numpy_now_singular", # Previously thought to be invertible
        {"matrix": [[1, 2, 3, 4], [2, 1, 4, 3], [3, 4, 1, 2], [4, 3, 2, 1]]},
        {"success": False, "result": None, "error": "La matriz no es invertible (singular). Los pasos detallan el problema."}
    )
]

INVALID_INPUT_CASES_INVERSE = [
    (
        "non_square_2x3",
        {"matrix": [[1, 2, 3], [4, 5, 6]]},
        400,
        "cuadrada para calcular su inversa. Se recibió una matriz de 2x3"
    ),
    (
        "non_square_3x2",
        {"matrix": [[1,2],[3,4],[5,6]]},
        400,
        "cuadrada para calcular su inversa. Se recibió una matriz de 3x2"
    ),
    (
        "empty_matrix",
        {"matrix": []},
        400,
        "suministrada no puede estar vacía"
    ),
    (
        "matrix_with_empty_row",
        {"matrix": [[1,2],[]]},
        400,
        "no puede ser una lista vacía si otras filas tienen elementos"
    ),
    (
        "ragged_matrix",
        {"matrix": [[1,2,3],[4,5]]},
        400,
        "deben tener el mismo número de columnas. La fila 2 tiene 2 columnas, se esperaban 3"
    ),
    (
        "invalid_element_char",
        {"matrix": [["1","a"],["2","3"]]},
        400,
        "Valor de entrada inválido: 'a'. No es un número, fracción (ej: '1/2'), ni string numérico"
    ),
    (
        "invalid_fraction_format",
        {"matrix": [["1/2/3","1"],["2","3"]]},
        400,
        "Valor de fracción inválido: '1/2/3'"
    ),
    (
        "division_by_zero_in_fraction",
        {"matrix": [["1/0","1"],["2","3"]]},
        400,
        "Valor inválido: '1/0'. El denominador no puede ser cero en una fracción."
    ),
    (
        "matrix_too_large_5x5",
        {"matrix": [[1]*5 for _ in range(5)]},
        400,
        "limitada a matrices de hasta 4 filas. Se recibió una matriz con 5 filas"
    )
]

@pytest.mark.parametrize("test_name, payload, expected_response", VALID_INVERSE_CASES)
def test_calculate_inverse_valid(client, test_name, payload, expected_response):
    response = client.post("/operations/inverse", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == expected_response["success"]
    
    if expected_response["result"] is not None:
        assert len(data["result"]) == len(expected_response["result"])
        for i in range(len(data["result"])):
            assert len(data["result"][i]) == len(expected_response["result"][i])
            for j in range(len(data["result"][i])):
                # Convert to string for consistent comparison, as results can be int or str fractions
                assert str(data["result"][i][j]) == str(expected_response["result"][i][j])
    else:
        assert data["result"] is None
        
    assert data["error"] == expected_response["error"]
    # Optionally, check if steps are present and non-empty if expected
    # For inverse, steps can be quite long, so we might just check for their existence
    if data["success"]:
        assert "steps" in data and isinstance(data["steps"], list) and len(data["steps"]) > 0


@pytest.mark.parametrize("test_name, payload, expected_response", SINGULAR_MATRIX_CASES)
def test_calculate_inverse_singular(client, test_name, payload, expected_response):
    response = client.post("/operations/inverse", json=payload)
    assert response.status_code == 200 # Custom validation errors return 200 with success:false
    data = response.json()
    assert data["success"] == expected_response["success"]
    assert data["result"] == expected_response["result"]
    assert data["error"] == expected_response["error"]
    # Steps might be present detailing why it's singular, so we don't assert their absence strictly.
    # We can assert that if steps are present, they are a list.
    if "steps" in data:
        assert isinstance(data["steps"], list)


@pytest.mark.parametrize("test_name, payload, expected_status_code, expected_error_detail_segment", INVALID_INPUT_CASES_INVERSE)
def test_calculate_inverse_invalid_input(client, test_name, payload, expected_status_code, expected_error_detail_segment):
    response = client.post("/operations/inverse", json=payload)
    assert response.status_code == expected_status_code
    
    data = response.json()
    # For 400 errors, FastAPI often puts the detail directly in data["detail"]
    # For Pydantic errors (which might lead to 422, but here we expect 400 for custom validation),
    # the structure might be more nested. We adjust to primarily check data["detail"] or data["error"]
    error_message_found = False
    if "detail" in data:
        if isinstance(data["detail"], str) and expected_error_detail_segment in data["detail"]:
            error_message_found = True
        elif isinstance(data["detail"], list):
            for error_item in data["detail"]:
                if isinstance(error_item, dict) and "msg" in error_item and expected_error_detail_segment in error_item["msg"]:
                    error_message_found = True
                    break
                elif isinstance(error_item, str) and expected_error_detail_segment in error_item:
                    error_message_found = True
                    break
    elif "error" in data and data["error"] and expected_error_detail_segment in data["error"]:
        error_message_found = True

    assert error_message_found, f"Expected error segment '{expected_error_detail_segment}' not found in response: {data}" 