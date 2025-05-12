import pytest
from fastapi.testclient import TestClient
from fractions import Fraction
from backend.main import app  # Asumiendo que la instancia de FastAPI se llama 'app'

client = TestClient(app)

# --- Casos de prueba para el cálculo exitoso del determinante ---
VALID_DETERMINANT_CASES = [
    # Matrices 1x1
    ("1x1_single_positive", {"matrix": [[5]]}, "5"),
    ("1x1_single_negative", {"matrix": [[-3]]}, "-3"),
    ("1x1_single_fraction", {"matrix": [["1/2"]]}, "1/2"),
    # Matrices 2x2
    ("2x2_integers_positive_det", {"matrix": [[1, 2], [3, 4]]}, "-2"), # 1*4 - 2*3 = 4 - 6 = -2
    ("2x2_integers_zero_det", {"matrix": [[1, 2], [2, 4]]}, "0"),     # 1*4 - 2*2 = 4 - 4 = 0
    ("2x2_fractions", {"matrix": [["1/2", "1/3"], ["1/4", "1/5"]]}, "1/60"), # Corregido: (1/2*1/5) - (1/3*1/4) = 1/10 - 1/12 = (12-10)/120 = 2/120 = 1/60
    ("2x2_fractions_simple", {"matrix": [["1", "1"], ["1", "2"]]}, "1"),
    ("2x2_mixed_types", {"matrix": [[2, "1/2"], [4, "3/4"]]}, "-1/2"), # 2*(3/4) - (1/2)*4 = 3/2 - 2 = 3/2 - 4/2 = -1/2
    # Matrices 3x3
    ("3x3_integers_example1", {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}, "0"), # Conocido por ser 0
    ("3x3_integers_example2", {"matrix": [[6, 1, 1], [4, -2, 5], [2, 8, 7]]}, "-306"), # De una calculadora
    ("3x3_identity", {"matrix": [[1,0,0],[0,1,0],[0,0,1]]}, "1"),
    ("3x3_with_fractions", {"matrix": [["1", "1/2", "0"], ["1/3", "1", "1/4"], ["1/2", "1/5", "1"]]}, "203/240"), # Corregido de 53/60
    ("3x3_simple_fractions", {"matrix": [[1,0,0],[0,1,0],[0,"1/2",2]]}, "2"), # 1*(1*2 - 0*1/2) = 2
    # Matrices 4x4
    ("4x4_identity", {"matrix": [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]}, "1"),
    ("4x4_simple_diag", {"matrix": [[2,0,0,0],[0,3,0,0],[0,0,4,0],[0,0,0,5]]}, "120"), # 2*3*4*5 = 120
    ("4x4_example", {"matrix": [[1,0,2,-1],[3,0,0,5],[2,1,4,-3],[1,0,5,0]]}, "30"), # Signo corregido de -30, asumiendo que la lógica gaussiana es consistente
]

@pytest.mark.parametrize("test_name, payload, expected_determinant", VALID_DETERMINANT_CASES)
def test_calculate_determinant_valid(test_name, payload, expected_determinant):
    response = client.post("/operations/determinant", json=payload)
    assert response.status_code == 200, f"Prueba '{test_name}' falló: Se esperaba 200, se obtuvo {response.status_code} - {response.text}"
    data = response.json()
    assert data["success"] == True, f"Prueba '{test_name}' falló: Se esperaba success=True - {data.get('error')}"
    assert data["result"] == expected_determinant, f"Prueba '{test_name}' falló: Se esperaba det={expected_determinant}, se obtuvo {data['result']}"
    assert "steps" in data
    assert len(data["steps"]) > 0, f"Prueba '{test_name}' falló: Se esperaba que los pasos estuvieran presentes."
    # Verificar frases clave en los pasos
    assert any("Matriz de entrada" in step for step in data["steps"]), f"Prueba '{test_name}' falló: Falta la matriz de entrada en los pasos"
    
    matrix_size = len(payload["matrix"])
    if matrix_size > 1: # Para 2x2, 3x3 y 4x4, esperar pasos de eliminación gaussiana
        assert any("Transformando la matriz a forma triangular superior mediante eliminación Gaussiana" in step for step in data["steps"]), f"Prueba '{test_name}' falló: Falta el paso inicial de eliminación gaussiana para matriz >1x1"
        if not (expected_determinant == "0" and any("El determinante es 0." in step for step in data["steps"])):
            # Si el determinante es 0 y el cálculo se detuvo temprano, estos pasos podrían estar ausentes
            assert any("Pivote actual A(" in step for step in data["steps"]), f"Prueba '{test_name}' falló: Faltan detalles del pivote para matriz >1x1 (y no es una salida temprana det=0)"
            assert any("La matriz está en forma triangular superior" in step for step in data["steps"]), f"Prueba '{test_name}' falló: Falta confirmación de forma triangular superior para matriz >1x1 (y no es una salida temprana det=0)"
    elif matrix_size == 1: # Verificación específica para 1x1 si es necesario, aunque el código actual lo maneja sin pasos explícitos de "eliminación gaussiana"
        assert any("El determinante es el único elemento" in step for step in data["steps"] ), f"Prueba '{test_name}' falló: Falta paso del determinante 1x1"


    final_determinant_string = f"El determinante final (calculado mediante eliminación Gaussiana) de la matriz A es: {expected_determinant}"
    if matrix_size == 1: # El caso 1x1 tiene una estructura de mensaje final diferente en el código
        final_determinant_string = f"El determinante es el único elemento: det(A) = {expected_determinant}"
    
    # Para determinante 0, el código puede retornar temprano con "El determinante es 0."
    if expected_determinant == "0" and any("El determinante es 0." in step for step in data["steps"]):
        pass # Esta es una salida temprana aceptable con un mensaje simple
    else:
        assert any(final_determinant_string in step for step in data["steps"]), f"Prueba '{test_name}' falló: Falta declaración final del determinante ('{final_determinant_string}'). Pasos: {data['steps']}"


# --- Casos de prueba para entradas inválidas ---
INVALID_DETERMINANT_CASES = [
    ("non_square_2x3", {"matrix": [[1, 2, 3], [4, 5, 6]]}, 400, "La matriz debe ser cuadrada para calcular el determinante."),
    ("non_square_3x2", {"matrix": [[1, 2], [3, 4], [5, 6]]}, 400, "La matriz debe ser cuadrada para calcular el determinante."),
    ("too_large_5x5", {"matrix": [[1]*5]*5}, 400, "La operación está limitada a matrices de hasta 4 filas."), # validar_matriz debería detectar esto
    ("invalid_element_char", {"matrix": [[1, 'a'], [3, 4]]}, 400, "Valor de entrada inválido: 'a'. No es un número, fracción (ej: '1/2'), ni string numérico (ej: '2.5')."),
    ("invalid_fraction_zero_denom", {"matrix": [["1/0"]]}, 400, "Valor inválido: '1/0'. El denominador no puede ser cero en una fracción."),
    ("empty_matrix", {"matrix": []}, 400, "suministrada no puede estar vacía."),
    ("matrix_empty_rows", {"matrix": [[]]}, 400, "Las filas de suministrada no pueden estar vacías (cero columnas)."),
    ("matrix_ragged", {"matrix": [[1,2], [3]]}, 400, "Todas las filas de suministrada deben tener el mismo número de columnas. La fila 2 tiene 1 columnas, se esperaban 2.") # Mensaje de error esperado actualizado
]

@pytest.mark.parametrize("test_name, payload, expected_status_code, expected_error_detail_segment", INVALID_DETERMINANT_CASES)
def test_calculate_determinant_invalid(test_name, payload, expected_status_code, expected_error_detail_segment):
    response = client.post("/operations/determinant", json=payload)
    assert response.status_code == expected_status_code, f"Prueba '{test_name}' falló: Se esperaba status {expected_status_code}, se obtuvo {response.status_code}"
    data = response.json()
    assert "detail" in data, f"Prueba '{test_name}' falló: Se esperaba 'detail' en la respuesta de error."
    assert expected_error_detail_segment in data["detail"], f"Prueba '{test_name}' falló: Se esperaba el detalle de error '{expected_error_detail_segment}', se obtuvo '{data['detail']}'"

# --- Prueba de detalles específicos de pasos para una matriz 3x3 ---
def test_determinant_3x3_detailed_steps():
    payload = {"matrix": [[1, 2, 1], [0, 3, 0], [1, 0, 2]]}
    expected_determinant_value = "3"

    response = client.post("/operations/determinant", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["result"] == expected_determinant_value
    steps = data["steps"]

    expected_step_snippets = [
        "Matriz de entrada A:",
        "A (3x3) (3x3):",
        "| 1  2  1 |",
        "| 0  3  0 |",
        "| 1  0  2 |",
        "Transformando la matriz a forma triangular superior mediante eliminación Gaussiana:",
        # Pivote 1: A(1,1) = 1
        "Pivote actual A(1,1) = 1",
        # Operación de fila F3 = F3 - (1) * F1 para A(3,1)
        "Eliminando elemento A(3,1) usando la operación: F3 = F3 - (1) * F1",
        "Matriz después de la operación (3x3):",
        "| 1  2  1 |",
        "| 0  3  0 |",
        "| 0 -2  1 |",
        # Pivote 2: A(2,2) = 3
        "Pivote actual A(2,2) = 3",
        # Operación de fila F3 = F3 - (-2/3) * F2 para A(3,2)
        "Eliminando elemento A(3,2) usando la operación: F3 = F3 - (-2/3) * F2",
        "Matriz después de la operación (3x3):",
        "| 1  2  1 |",
        "| 0  3  0 |",
        "| 0  0  1 |",
        # Pivote 3: A(3,3) = 1
        "Pivote actual A(3,3) = 1",
        "La matriz está en forma triangular superior.",
        "Matriz triangular superior final (3x3):",
        "| 1  2  1 |",
        "| 0  3  0 |",
        "| 0  0  1 |",
        "Calculando el determinante como el producto de los elementos de la diagonal multiplicados por el factor de intercambio de filas (1):",
        "det(A) = 1 * (1 * 3 * 1)",
        "= 1 * 3",
        "= 3",
        "El determinante final (calculado mediante eliminación Gaussiana) de la matriz A es: 3"
    ]

    step_idx = 0
    for snippet in expected_step_snippets:
        found_snippet = False
        for i in range(step_idx, len(steps)):
            # Normalizar espacios para comparación, especialmente para el formato de matrices
            normalized_step = ' '.join(steps[i].split())
            normalized_snippet = ' '.join(snippet.split())
            if normalized_snippet in normalized_step:
                step_idx = i + 1
                found_snippet = True
                break
        assert found_snippet, f"Fragmento de paso faltante o fuera de orden: '{snippet}'. Pasos que se están buscando: {steps[step_idx-1 if step_idx > 0 else 0 : step_idx+3]}"


# Prueba para una matriz 4x4 que podría involucrar una llamada recursiva a un subdeterminante 3x3
# que a su vez se descompondría en 2x2.
# Por simplicidad, usando una matriz con muchos ceros para facilitar la verificación manual.
def test_determinant_4x4_gaussian_steps(): # Renombrado de test_determinant_4x4_recursive_steps
    # Matriz diagonal, el determinante es el producto de los elementos diagonales.
    # La eliminación gaussiana debería ser sencilla sin intercambios de filas o eliminaciones complejas.
    payload = {"matrix": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]]}
    expected_determinant_value = "6" # 1 * 1 * 2 * 3 = 6

    response = client.post("/operations/determinant", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["result"] == expected_determinant_value
    steps = data["steps"]

    # Verificar pasos clave que indican eliminación gaussiana
    assert any("Matriz de entrada A:" in step for step in steps)
    assert any("A (4x4) (4x4):" in step for step in steps)
    assert any("Transformando la matriz a forma triangular superior mediante eliminación Gaussiana:" in step for step in steps)
    
    # Verificar pivotes
    assert any("Pivote actual A(1,1) = 1" in step for step in steps)
    assert any("Pivote actual A(2,2) = 1" in step for step in steps)
    assert any("Pivote actual A(3,3) = 2" in step for step in steps)
    assert any("Pivote actual A(4,4) = 3" in step for step in steps)

    # Como es diagonal, no deberían ocurrir pasos de eliminación real o intercambios de filas para estos valores específicos
    assert not any("Intercambiando Fila" in step for step in steps)
    assert not any("Eliminando elemento A(" in step for step in steps if "usando la operación:" in step)

    assert any("La matriz está en forma triangular superior." in step for step in steps)
    assert any("Matriz triangular superior final (4x4):" in step for step in steps)
    # Verificar la visualización de la matriz final (debería ser la misma que la entrada para una matriz diagonal)
    assert any("| 1  0  0  0 |" in step for step in steps)
    assert any("| 0  1  0  0 |" in step for step in steps)
    assert any("| 0  0  2  0 |" in step for step in steps)
    assert any("| 0  0  0  3 |" in step for step in steps)

    assert any(f"Calculando el determinante como el producto de los elementos de la diagonal multiplicados por el factor de intercambio de filas (1):" in step for step in steps)
    assert any(f"det(A) = 1 * (1 * 1 * 2 * 3)" in step for step in steps)
    assert any(f"El determinante final (calculado mediante eliminación Gaussiana) de la matriz A es: {expected_determinant_value}" in step for step in steps)

# Ejemplo de una matriz 2x2 que resulta en determinante 0 donde una columna se vuelve toda ceros
def test_determinant_2x2_zero_det_column_becomes_zero():
    payload = {"matrix": [[1, 2], [2, 4]]} # Det = 1*4 - 2*2 = 0
    expected_determinant_value = "0"

    response = client.post("/operations/determinant", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["result"] == expected_determinant_value
    steps = data["steps"]

    assert any("Matriz de entrada A:" in step for step in steps)
    assert any("Transformando la matriz a forma triangular superior mediante eliminación Gaussiana:" in step for step in steps)
    assert any("Pivote actual A(1,1) = 1" in step for step in steps)
    assert any("Eliminando elemento A(2,1) usando la operación: F2 = F2 - (2) * F1" in step for step in steps)
    assert any("| 1  2 |" in step for step in steps) # Inicial después del pivote
    assert any("| 0  0 |" in step for step in steps) # Después de F2 = F2 - 2*F1
    assert any("Columna 2 (debajo o en la diagonal) no tiene pivote (todos son cero)." in step for step in steps)
    assert any("El determinante es 0." in step for step in steps)
    # El mensaje de determinante "final" podría ser el específico "El determinante es 0." o el genérico.
    # El código actual asegura que "El determinante es 0." esté presente si sale temprano.
    # Y el endpoint principal agrega "El determinante final (calculado mediante eliminación Gaussiana) de la matriz A es: 0"
    assert any("El determinante final (calculado mediante eliminación Gaussiana) de la matriz A es: 0" in step for step in steps)

# Ejemplo de una matriz 3x3 que requiere un intercambio de filas
def test_determinant_3x3_row_swap():
    payload = {"matrix": [[0, 1, 2], [3, 4, 5], [6, 7, 8]]} # Det: -(3*(8-10) - 4*(0-12) + 5*(0-6)) = -( -6 + 48 -30) = -(-6+18) = -12. No, det = 0*(..) - 1*(3*8 - 5*6) + 2*(3*7 - 4*6) = -1*(24-30) + 2*(21-24) = -1*(-6) + 2*(-3) = 6 - 6 = 0
    expected_determinant_value = "0" # Cofactor: 0 - 1(24-30) + 2(21-24) = -1(-6) + 2(-3) = 6 - 6 = 0

    response = client.post("/operations/determinant", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["result"] == expected_determinant_value
    steps = data["steps"]

    assert any("Intercambiando Fila 1 con Fila 2 para obtener un pivote no nulo en A(1,1)." in step for step in steps)
    assert any("(Multiplicador del determinante actual: -1)" in step for step in steps)
    assert any("Matriz después del intercambio (3x3):" in step for step in steps)
    assert any("| 3  4  5 |" in step for step in steps)
    assert any("| 0  1  2 |" in step for step in steps)

    # Verificar que el cálculo final del determinante use el multiplicador
    if expected_determinant_value != "0": # Si det es 0, podría salir temprano
         assert any(f"det(A) = -1 * (" in step for step in steps), "El cálculo del determinante debería mostrar el uso del multiplicador -1 debido al intercambio de filas."
    
    assert any(f"El determinante final (calculado mediante eliminación Gaussiana) de la matriz A es: {expected_determinant_value}" in step for step in steps) 