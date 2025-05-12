import json # Para impresión detallada

# Pruebas que se centran en el éxito de la operación de suma con diferentes entradas y tamaños válidos.
# Se asume que la lógica de validación compartida (dimensiones, estructura, etc.)
# está cubierta en test_shared_validations.py

def test_add_matrices_success(client):
    """Prueba la suma de matrices válidas y compatibles (con enteros)."""
    print("\n--- test_add_matrices_success (in test_addition.py) ---")
    payload = {
        "matrix_a": [[1, 2], [3, 4]],
        "matrix_b": [[5, 6], [7, 8]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    assert response.status_code == 200
    assert data["success"] is True
    # Comparar elementos como strings para manejar la API que devuelve números como strings
    expected_result_str = [[str(el) for el in row] for row in [[6, 8], [10, 12]]]
    assert data["result"] == expected_result_str
    assert "Matriz A (2x2):" in data["steps"]
    assert "  | 1  2 |" in data["steps"]
    assert "  | 3  4 |" in data["steps"]
    assert "Matriz B (2x2):" in data["steps"]
    assert "  | 5  6 |" in data["steps"]
    assert "  | 7  8 |" in data["steps"]
    assert "  C(1,1) = A(1,1) + B(1,1) = 1 + 5 = 6" in data["steps"]
    assert "Suma completada." in data["steps"]

def test_add_matrices_success_float_and_int_inputs(client):
    """Prueba la suma con entradas float e int que se convierten a Fraction."""
    print("\n--- test_add_matrices_success_float_and_int_inputs (in test_addition.py) ---")
    payload = {
        "matrix_a": [[1, 2.5], [3, "4.0"]], 
        "matrix_b": [[5, "1/2"], ["7/1", 8]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    assert response.status_code == 200
    assert data["success"] is True
    # Comparar elementos como strings
    expected_result_str = [[str(el) for el in row] for row in [[6, 3], [10, 12]]]
    assert data["result"] == expected_result_str
    assert "  | 1  5/2 |" in data["steps"]
    assert "  | 3    4 |" in data["steps"] 
    assert "  | 5  1/2 |" in data["steps"]
    assert "  | 7    8 |" in data["steps"]
    assert "  C(1,2) = A(1,2) + B(1,2) = 5/2 + 1/2 = 3" in data["steps"]

def test_add_matrices_success_fractional_inputs_and_results(client):
    """Prueba la suma con entradas fraccionarias y resultados fraccionarios/enteros."""
    print("\n--- test_add_matrices_success_fractional_inputs_and_results (in test_addition.py) ---")
    payload = {
        "matrix_a": [["1/2", "3/4"], ["-1/5", 2]],
        "matrix_b": [["1/4", "1/4"], ["3/5", "-1/1"]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    assert response.status_code == 200
    assert data["success"] is True
    # Comparar elementos como strings. Las fracciones ya son strings, los enteros necesitan conversión.
    expected_result_str = [[str(el) if not isinstance(el, str) else el for el in row] for row in [["3/4", 1], ["2/5", 1]]]
    assert data["result"] == expected_result_str
    assert "  |  1/2  3/4 |" in data["steps"]
    assert "  | -1/5    2 |" in data["steps"]
    assert "  | 1/4  1/4 |" in data["steps"]
    assert "  | 3/5   -1 |" in data["steps"]
    assert "  C(2,1) = A(2,1) + B(2,1) = -1/5 + 3/5 = 2/5" in data["steps"]

def test_add_matrices_flexible_fraction_input(client):
    """Prueba la suma con entradas de fracción formateadas flexiblemente."""
    print("\n--- test_add_matrices_flexible_fraction_input (in test_addition.py) ---")
    payload = {
        "matrix_a": [[" 1/2 ", "3 / 4"], [" -1 / 5 ", 2]],
        "matrix_b": [["1/4", " 1 / 4"], ["3/5", "-1 / 1"]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    assert response.status_code == 200
    assert data["success"] is True
    # Comparar elementos como strings
    expected_result_str = [[str(el) for el in row] for row in [["3/4", 1], ["2/5", 1]]]
    assert data["result"] == expected_result_str
    assert "  |  1/2  3/4 |" in data["steps"]
    assert "  C(1,1) = A(1,1) + B(1,1) = 1/2 + 1/4 = 3/4" in data["steps"]

def test_add_matrices_various_square_sizes(client):
    """Prueba la suma de matrices cuadradas de varios tamaños válidos (1x1, 3x3, 4x4)."""
    print("\n--- test_add_matrices_various_square_sizes (in test_addition.py) ---")
    test_cases = [
        {"size_desc": "1x1", "a": [[1]], "b": [[2]], "expected": [[3]], "a_disp": ["Matriz A (1x1):", "  | 1 |"], "b_disp": ["Matriz B (1x1):", "  | 2 |"], "calc_steps": ["  C(1,1) = A(1,1) + B(1,1) = 1 + 2 = 3"]},
        {"size_desc": "3x3", 
         "a": [[1,2,3],[4,5,6],[7,8,9]], "b": [[9,8,7],[6,5,4],[3,2,1]], "expected": [[10,10,10],[10,10,10],[10,10,10]],
         "a_disp": ["Matriz A (3x3):", "  | 1  2  3 |", "  | 4  5  6 |", "  | 7  8  9 |"],
         "b_disp": ["Matriz B (3x3):", "  | 9  8  7 |", "  | 6  5  4 |", "  | 3  2  1 |"],
         "calc_steps": [
             "  C(1,1) = A(1,1) + B(1,1) = 1 + 9 = 10", "  C(1,2) = A(1,2) + B(1,2) = 2 + 8 = 10", "  C(1,3) = A(1,3) + B(1,3) = 3 + 7 = 10",
             "  C(2,1) = A(2,1) + B(2,1) = 4 + 6 = 10", "  C(2,2) = A(2,2) + B(2,2) = 5 + 5 = 10", "  C(2,3) = A(2,3) + B(2,3) = 6 + 4 = 10",
             "  C(3,1) = A(3,1) + B(3,1) = 7 + 3 = 10", "  C(3,2) = A(3,2) + B(3,2) = 8 + 2 = 10", "  C(3,3) = A(3,3) + B(3,3) = 9 + 1 = 10",
         ]},
        {"size_desc": "4x4", 
         "a": [[1]*4]*4, "b": [[2]*4]*4, "expected": [[3]*4]*4,
         "a_disp": ["Matriz A (4x4):"] + ["  | 1  1  1  1 |" for _ in range(4)],
         "b_disp": ["Matriz B (4x4):"] + ["  | 2  2  2  2 |" for _ in range(4)],
         "calc_steps": [f"  C({i+1},{j+1}) = A({i+1},{j+1}) + B({i+1},{j+1}) = 1 + 2 = 3" for i in range(4) for j in range(4)]
        },
    ]
    for case in test_cases:
        print(f"\nTesting {case['size_desc']}")
        payload = {"matrix_a": case["a"], "matrix_b": case["b"]}
        response = client.post("/operations/add", json=payload)
        data = response.json()
        # print(json.dumps(data, indent=2, ensure_ascii=False)) # Opcional: para vista detallada durante la depuración
        assert response.status_code == 200, f"{case['size_desc']} failed status code"
        assert data["success"] is True, f"{case['size_desc']} failed success"
        # Comparar elementos como strings
        expected_result_str = [[str(el) if not isinstance(el, str) else el for el in row] for row in case["expected"]]
        assert data["result"] == expected_result_str, f"{case['size_desc']} failed result"
        for step in case["a_disp"]:
            assert step in data["steps"], f"{case['size_desc']} missing step for A: {step}"
        for step in case["b_disp"]:
            assert step in data["steps"], f"{case['size_desc']} missing step for B: {step}"
        for step in case["calc_steps"]:
            assert step in data["steps"], f"{case['size_desc']} missing calculation step: {step}"
        assert "Suma completada." in data["steps"]

def test_add_matrices_various_rectangular_sizes(client):
    """Prueba la suma de matrices rectangulares de varios tamaños válidos."""
    print("\n--- test_add_matrices_various_rectangular_sizes (in test_addition.py) ---")
    test_cases = [
        {"size_desc": "1x4", "a": [[1,1,1,1]], "b": [[2,2,2,2]], "expected": [[3,3,3,3]],
         "a_disp": ["Matriz A (1x4):", "  | 1  1  1  1 |"], "b_disp": ["Matriz B (1x4):", "  | 2  2  2  2 |"],
         "calc_steps": ["  C(1,1) = A(1,1) + B(1,1) = 1 + 2 = 3", "  C(1,2) = A(1,2) + B(1,2) = 1 + 2 = 3", "  C(1,3) = A(1,3) + B(1,3) = 1 + 2 = 3", "  C(1,4) = A(1,4) + B(1,4) = 1 + 2 = 3"]},
        {"size_desc": "4x1", "a": [[1],[1],[1],[1]], "b": [[2],[2],[2],[2]], "expected": [[3],[3],[3],[3]],
         "a_disp": ["Matriz A (4x1):"] + ["  | 1 |" for _ in range(4)],
         "b_disp": ["Matriz B (4x1):"] + ["  | 2 |" for _ in range(4)],
         "calc_steps": [f"  C({i+1},1) = A({i+1},1) + B({i+1},1) = 1 + 2 = 3" for i in range(4)]},
        {"size_desc": "2x3", "a": [[1,1,1],[1,1,1]], "b": [[2,2,2],[2,2,2]], "expected": [[3,3,3],[3,3,3]],
         "a_disp": ["Matriz A (2x3):", "  | 1  1  1 |", "  | 1  1  1 |"],
         "b_disp": ["Matriz B (2x3):", "  | 2  2  2 |", "  | 2  2  2 |"],
         "calc_steps": [f"  C({i+1},{j+1}) = A({i+1},{j+1}) + B({i+1},{j+1}) = 1 + 2 = 3" for i in range(2) for j in range(3)]},
    ]
    for case in test_cases:
        print(f"\nTesting {case['size_desc']}")
        payload = {"matrix_a": case["a"], "matrix_b": case["b"]}
        response = client.post("/operations/add", json=payload)
        data = response.json()
        # print(json.dumps(data, indent=2, ensure_ascii=False))
        assert response.status_code == 200, f"{case['size_desc']} failed status code"
        assert data["success"] is True, f"{case['size_desc']} failed success"
        # Comparar elementos como strings
        expected_result_str = [[str(el) if not isinstance(el, str) else el for el in row] for row in case["expected"]]
        assert data["result"] == expected_result_str, f"{case['size_desc']} failed result"
        for step in case["a_disp"]:
            assert step in data["steps"], f"{case['size_desc']} missing step for A: {step}"
        for step in case["b_disp"]:
            assert step in data["steps"], f"{case['size_desc']} missing step for B: {step}"
        for step in case["calc_steps"]:
            assert step in data["steps"], f"{case['size_desc']} missing calculation step: {step}"
        assert "Suma completada." in data["steps"] 