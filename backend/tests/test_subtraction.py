import json # For pretty printing

# Tests that focus on the success of the subtraction operation with various valid inputs and sizes.
# It's assumed that shared validation logic (dimensions, structure, etc.) 
# is covered in test_shared_validations.py

def test_subtract_matrices_success(client):
    """Prueba la resta de matrices válidas y compatibles (con enteros)."""
    print("\n--- test_subtract_matrices_success (in test_subtraction.py) ---")
    payload = {
        "matrix_a": [[5, 8], [10, 12]],
        "matrix_b": [[1, 2], [3, 4]]
    }
    response = client.post("/operations/subtract", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    assert response.status_code == 200
    assert data["success"] is True
    # Compare elements as strings
    expected_result_str = [[str(el) for el in row] for row in [[4, 6], [7, 8]]]
    assert data["result"] == expected_result_str
    assert "Matriz A (2x2):" in data["steps"]
    assert "  |  5   8 |" in data["steps"]
    assert "  | 10  12 |" in data["steps"]
    assert "Matriz B (2x2):" in data["steps"]
    assert "  | 1  2 |" in data["steps"]
    assert "  | 3  4 |" in data["steps"]
    assert "  C(1,1) = A(1,1) - B(1,1) = 5 - 1 = 4" in data["steps"]
    assert "Resta completada." in data["steps"]

def test_subtract_matrices_success_float_and_int_inputs(client):
    """Prueba la resta con entradas float e int que se convierten a Fraction."""
    print("\n--- test_subtract_matrices_success_float_and_int_inputs (in test_subtraction.py) ---")
    payload = {
        "matrix_a": [[6, 3], [10, "12.0"]],      
        "matrix_b": [[1, "2.5"], ["3/1", 4]] 
    }
    response = client.post("/operations/subtract", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    assert response.status_code == 200
    assert data["success"] is True
    # Compare elements as strings. Fractions are already strings, integers need conversion.
    expected_result_str = [[str(el) if not isinstance(el, str) else el for el in row] for row in [[5, "1/2"], [7, 8]]]
    assert data["result"] == expected_result_str
    assert "  |  6   3 |" in data["steps"]
    assert "  | 10  12 |" in data["steps"] 
    assert "  | 1  5/2 |" in data["steps"]
    assert "  | 3    4 |" in data["steps"]
    assert "  C(1,2) = A(1,2) - B(1,2) = 3 - 5/2 = 1/2" in data["steps"]

def test_subtract_matrices_success_fractional_inputs_and_results(client):
    """Prueba la resta con entradas fraccionarias y resultados fraccionarios/enteros."""
    print("\n--- test_subtract_matrices_success_fractional_inputs_and_results (in test_subtraction.py) ---")
    payload = {
        "matrix_a": [["3/4", 1], ["2/5", 1]],
        "matrix_b": [["1/4", "1/4"], ["-1/5", "-1/1"]]
    }
    response = client.post("/operations/subtract", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    assert response.status_code == 200
    assert data["success"] is True
    # Compare elements as strings
    expected_result_str = [[str(el) if not isinstance(el, str) else el for el in row] for row in [["1/2", "3/4"], ["3/5", 2]]]
    assert data["result"] == expected_result_str
    assert "  | 3/4  1 |" in data["steps"]
    assert "  | 2/5  1 |" in data["steps"]
    assert "  |  1/4  1/4 |" in data["steps"]
    assert "  | -1/5   -1 |" in data["steps"]
    assert "  C(2,2) = A(2,2) - B(2,2) = 1 - -1 = 2" in data["steps"]

def test_subtract_matrices_flexible_fraction_input(client):
    """Prueba la resta con entradas de fracción formateadas flexiblemente."""
    print("\n--- test_subtract_matrices_flexible_fraction_input (in test_subtraction.py) ---")
    payload = {
        "matrix_a": [[" 3/4 ", "1 / 1"], [" 2 / 5 ", " 1"]],
        "matrix_b": [["1/4", " 1 / 4"], ["-1 / 5", "-1 / 1"]]
    }
    response = client.post("/operations/subtract", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    assert response.status_code == 200
    assert data["success"] is True
    # Compare elements as strings
    expected_result_str = [[str(el) if not isinstance(el, str) else el for el in row] for row in [["1/2", "3/4"], ["3/5", 2]]]
    assert data["result"] == expected_result_str
    assert "  | 3/4  1 |" in data["steps"]
    assert "  C(1,1) = A(1,1) - B(1,1) = 3/4 - 1/4 = 1/2" in data["steps"]

def test_subtract_matrices_various_square_sizes(client):
    """Prueba la resta de matrices cuadradas de varios tamaños válidos (1x1, 3x3, 4x4)."""
    print("\n--- test_subtract_matrices_various_square_sizes (in test_subtraction.py) ---")
    test_cases = [
        {"size_desc": "1x1", "a": [[3]], "b": [[2]], "expected": [[1]], "a_disp": ["Matriz A (1x1):", "  | 3 |"], "b_disp": ["Matriz B (1x1):", "  | 2 |"], "calc_steps": ["  C(1,1) = A(1,1) - B(1,1) = 3 - 2 = 1"]},
        {"size_desc": "3x3", 
         "a": [[10,10,10],[10,10,10],[10,10,10]], "b": [[9,8,7],[6,5,4],[3,2,1]], "expected": [[1,2,3],[4,5,6],[7,8,9]],
         "a_disp": ["Matriz A (3x3):", "  | 10  10  10 |", "  | 10  10  10 |", "  | 10  10  10 |"],
         "b_disp": ["Matriz B (3x3):", "  | 9  8  7 |", "  | 6  5  4 |", "  | 3  2  1 |"],
         "calc_steps": [
             "  C(1,1) = A(1,1) - B(1,1) = 10 - 9 = 1", "  C(1,2) = A(1,2) - B(1,2) = 10 - 8 = 2", "  C(1,3) = A(1,3) - B(1,3) = 10 - 7 = 3",
             "  C(2,1) = A(2,1) - B(2,1) = 10 - 6 = 4", "  C(2,2) = A(2,2) - B(2,2) = 10 - 5 = 5", "  C(2,3) = A(2,3) - B(2,3) = 10 - 4 = 6",
             "  C(3,1) = A(3,1) - B(3,1) = 10 - 3 = 7", "  C(3,2) = A(3,2) - B(3,2) = 10 - 2 = 8", "  C(3,3) = A(3,3) - B(3,3) = 10 - 1 = 9",
         ]},
        {"size_desc": "4x4", 
         "a": [[3]*4]*4, "b": [[1]*4]*4, "expected": [[2]*4]*4,
         "a_disp": ["Matriz A (4x4):"] + ["  | 3  3  3  3 |" for _ in range(4)],
         "b_disp": ["Matriz B (4x4):"] + ["  | 1  1  1  1 |" for _ in range(4)],
         "calc_steps": [f"  C({i+1},{j+1}) = A({i+1},{j+1}) - B({i+1},{j+1}) = 3 - 1 = 2" for i in range(4) for j in range(4)]
        },
    ]
    for case in test_cases:
        print(f"\nTesting {case['size_desc']}")
        payload = {"matrix_a": case["a"], "matrix_b": case["b"]}
        response = client.post("/operations/subtract", json=payload)
        data = response.json()
        # print(json.dumps(data, indent=2, ensure_ascii=False))
        assert response.status_code == 200, f"{case['size_desc']} failed status code"
        assert data["success"] is True, f"{case['size_desc']} failed success"
        # Compare elements as strings
        expected_result_str = [[str(el) if not isinstance(el, str) else el for el in row] for row in case["expected"]]
        assert data["result"] == expected_result_str, f"{case['size_desc']} failed result"
        for step in case["a_disp"]:
            assert step in data["steps"], f"{case['size_desc']} missing step for A: {step}"
        for step in case["b_disp"]:
            assert step in data["steps"], f"{case['size_desc']} missing step for B: {step}"
        for step in case["calc_steps"]:
            assert step in data["steps"], f"{case['size_desc']} missing calculation step: {step}"
        assert "Resta completada." in data["steps"]

def test_subtract_matrices_various_rectangular_sizes(client):
    """Prueba la resta de matrices rectangulares de varios tamaños válidos."""
    print("\n--- test_subtract_matrices_various_rectangular_sizes (in test_subtraction.py) ---")
    test_cases = [
        {"size_desc": "1x4", "a": [[3,3,3,3]], "b": [[1,1,1,1]], "expected": [[2,2,2,2]],
         "a_disp": ["Matriz A (1x4):", "  | 3  3  3  3 |"], "b_disp": ["Matriz B (1x4):", "  | 1  1  1  1 |"],
         "calc_steps": ["  C(1,1) = A(1,1) - B(1,1) = 3 - 1 = 2", "  C(1,2) = A(1,2) - B(1,2) = 3 - 1 = 2", "  C(1,3) = A(1,3) - B(1,3) = 3 - 1 = 2", "  C(1,4) = A(1,4) - B(1,4) = 3 - 1 = 2"]},
        {"size_desc": "4x1", "a": [[3],[3],[3],[3]], "b": [[1],[1],[1],[1]], "expected": [[2],[2],[2],[2]],
         "a_disp": ["Matriz A (4x1):"] + ["  | 3 |" for _ in range(4)],
         "b_disp": ["Matriz B (4x1):"] + ["  | 1 |" for _ in range(4)],
         "calc_steps": [f"  C({i+1},1) = A({i+1},1) - B({i+1},1) = 3 - 1 = 2" for i in range(4)]},
        {"size_desc": "2x3", "a": [[3,3,3],[3,3,3]], "b": [[1,1,1],[1,1,1]], "expected": [[2,2,2],[2,2,2]],
         "a_disp": ["Matriz A (2x3):", "  | 3  3  3 |", "  | 3  3  3 |"],
         "b_disp": ["Matriz B (2x3):", "  | 1  1  1 |", "  | 1  1  1 |"],
         "calc_steps": [f"  C({i+1},{j+1}) = A({i+1},{j+1}) - B({i+1},{j+1}) = 3 - 1 = 2" for i in range(2) for j in range(3)]},
    ]
    for case in test_cases:
        print(f"\nTesting {case['size_desc']}")
        payload = {"matrix_a": case["a"], "matrix_b": case["b"]}
        response = client.post("/operations/subtract", json=payload)
        data = response.json()
        # print(json.dumps(data, indent=2, ensure_ascii=False))
        assert response.status_code == 200, f"{case['size_desc']} failed status code"
        assert data["success"] is True, f"{case['size_desc']} failed success"
        # Compare elements as strings
        expected_result_str = [[str(el) if not isinstance(el, str) else el for el in row] for row in case["expected"]]
        assert data["result"] == expected_result_str, f"{case['size_desc']} failed result"
        for step in case["a_disp"]:
            assert step in data["steps"], f"{case['size_desc']} missing step for A: {step}"
        for step in case["b_disp"]:
            assert step in data["steps"], f"{case['size_desc']} missing step for B: {step}"
        for step in case["calc_steps"]:
            assert step in data["steps"], f"{case['size_desc']} missing calculation step: {step}"
        assert "Resta completada." in data["steps"] 