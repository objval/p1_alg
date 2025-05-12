import json

# These tests verify shared validation logic: input type conversion/validation (to_fraction),
# structural matrix validation (validar_matriz), and dimension/size validation 
# (validar_dimensiones_para_suma_resta).
# They use the /operations/add endpoint as a vehicle to trigger these shared validations.
# The specific arithmetic operation (add vs subtract) is not the primary focus here.

# ---- Input Element Validation (to_fraction related) ----

def test_invalid_fraction_string_format(client):
    """Prueba una operación con una cadena de fracción malformada."""
    print("\n--- test_invalid_fraction_string_format (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [["1/2a", "3/4"]],
        "matrix_b": [["1/4", "1/4"]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200 # Custom error, not Pydantic
    assert data["success"] is False
    assert "Valor de entrada inválido: '1/2a'. No es un número, fracción (ej: '1/2'), ni string numérico (ej: '2.5')." in data["error"]

def test_division_by_zero_in_fraction(client):
    """Prueba una operación con una fracción que implica división por cero."""
    print("\n--- test_division_by_zero_in_fraction (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [["1 / 0", "3/4"]],
        "matrix_b": [["1/4", "1/4"]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200
    assert data["success"] is False
    assert "Valor inválido: '1 / 0'. El denominador no puede ser cero en una fracción." in data["error"]

def test_invalid_fraction_string_mixed_with_valid(client):
    """Prueba una operación con una cadena de fracción malformada mezclada con válidas."""
    print("\n--- test_invalid_fraction_string_mixed_with_valid (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [[1, "1/2"], ["bad/ format", 4]],
        "matrix_b": [[1,1],[1,1]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200
    assert data["success"] is False
    assert "Valor de entrada inválido: 'bad/ format'. No es un número, fracción (ej: '1/2'), ni string numérico (ej: '2.5')." in data["error"]

# ---- Matrix Dimension and Shape Validation (validar_dimensiones_para_suma_resta & validar_matriz) ----

def test_operation_dimension_mismatch_filas(client):
    """Prueba una operación (suma/resta) con diferente número de filas."""
    print("\n--- test_operation_dimension_mismatch_filas (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [[1, 2], [3, 4]],
        "matrix_b": [[5, 6]]
    }
    # Test with add endpoint
    response_add = client.post("/operations/add", json=payload)
    data_add = response_add.json()
    print("ADD:", json.dumps(data_add, indent=2, ensure_ascii=False))
    assert response_add.status_code == 200 
    assert data_add["success"] is False
    assert data_add["error"] == "Las matrices A y B deben tener el mismo número de filas para la suma/resta. A tiene 2 filas y B tiene 1 filas."
    
    # Test with subtract endpoint
    response_sub = client.post("/operations/subtract", json=payload)
    data_sub = response_sub.json()
    print("SUBTRACT:", json.dumps(data_sub, indent=2, ensure_ascii=False))
    assert response_sub.status_code == 200 
    assert data_sub["success"] is False
    assert data_sub["error"] == "Las matrices A y B deben tener el mismo número de filas para la suma/resta. A tiene 2 filas y B tiene 1 filas."

def test_operation_dimension_mismatch_columnas(client):
    """Prueba una operación (suma/resta) con diferente número de columnas."""
    print("\n--- test_operation_dimension_mismatch_columnas (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [[1, 2, 3], [4, 5, 6]],
        "matrix_b": [[1, 2], [3, 4]]
    }
    response = client.post("/operations/add", json=payload) # Using /add, but validation is shared
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200
    assert data["success"] is False
    assert data["error"] == "Las matrices A y B deben tener el mismo número de columnas para la suma/resta. A tiene 3 columnas y B tiene 2 columnas."

def test_operation_empty_matrix_a(client):
    """Prueba una operación con la matriz A vacía."""
    print("\n--- test_operation_empty_matrix_a (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [],
        "matrix_b": [[1, 2]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200
    assert data["success"] is False
    assert data["error"] == "La matriz A no puede estar vacía."

def test_operation_empty_matrix_b(client):
    """Prueba una operación con la matriz B vacía."""
    print("\n--- test_operation_empty_matrix_b (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [[1, 2]],
        "matrix_b": []
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200
    assert data["success"] is False
    assert data["error"] == "La matriz B no puede estar vacía."

def test_operation_empty_rows_in_a(client):
    """Prueba una operación con filas vacías en la matriz A."""
    print("\n--- test_operation_empty_rows_in_a (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [[]],
        "matrix_b": [[1,2]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200
    assert data["success"] is False
    assert "Las filas de la matriz a no pueden estar vacías (cero columnas)." in data["error"]

def test_operation_ragged_matrix_a(client):
    """Prueba una operación con matriz A no rectangular (ragged)."""
    print("\n--- test_operation_ragged_matrix_a (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [[1, 2], [3]],
        "matrix_b": [[4, 5], [6, 7]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200
    assert data["success"] is False
    assert "Todas las filas de la matriz a deben tener el mismo número de columnas" in data["error"]

def test_operation_max_size_exceeded_rows(client):
    """Prueba una operación con matrices que exceden el máximo de filas (4xN)."""
    print("\n--- test_operation_max_size_exceeded_rows (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [[1]*2 for _ in range(5)], 
        "matrix_b": [[1]*2 for _ in range(5)] 
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200
    assert data["success"] is False
    assert "La operación está limitada a matrices de hasta 4 filas." in data["error"]

def test_operation_max_size_exceeded_cols(client):
    """Prueba una operación con matrices que exceden el máximo de columnas (Nx5)."""
    print("\n--- test_operation_max_size_exceeded_cols (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [[1]*5 for _ in range(2)], 
        "matrix_b": [[1]*5 for _ in range(2)] 
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200
    assert data["success"] is False
    assert "La operación está limitada a matrices de hasta 4 columnas." in data["error"]

# ---- Pydantic Model & Custom Structural Validation ----

def test_matrix_input_first_row_not_list(client):
    """Prueba una operación donde la primera fila de una matriz no es una lista (Pydantic validation)."""
    print("\n--- test_matrix_input_first_row_not_list (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [None, [1,2]], # First row is None
        "matrix_b": [[1,1],[1,1]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 422 # Pydantic validation error
    assert data["detail"][0]["type"] == "list_type"
    assert data["detail"][0]["loc"] == ["body", "matrix_a", 0]
    assert "Input should be a valid list" in data["detail"][0]["msg"]

def test_matrix_input_subsequent_row_not_list(client):
    """Prueba una operación donde una fila subsiguiente no es una lista (Pydantic validation)."""
    print("\n--- test_matrix_input_subsequent_row_not_list (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [[1,2], None], # Second row is None
        "matrix_b": [[1,1],[1,1]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 422 # Pydantic validation error
    assert data["detail"][0]["type"] == "list_type"
    assert data["detail"][0]["loc"] == ["body", "matrix_a", 1]
    assert "Input should be a valid list" in data["detail"][0]["msg"]

def test_matrix_input_empty_row_after_content(client):
    """Prueba una operación donde una fila está vacía después de una fila con contenido (custom validation)."""
    print("\n--- test_matrix_input_empty_row_after_content (in test_shared_validations.py) ---")
    payload = {
        "matrix_a": [[1,2], []], # Second row is empty list
        "matrix_b": [[1,1],[1,1]]
    }
    response = client.post("/operations/add", json=payload)
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    assert response.status_code == 200 # Error from our custom validation
    assert data["success"] is False
    assert "La fila 2 de la matriz a no puede ser una lista vacía si otras filas tienen elementos." in data["error"] 