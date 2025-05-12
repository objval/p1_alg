# 📐 Calculadora de Álgebra Lineal MAT1187 – Requisitos Funcionales del API

## 🎯 Propósito del Proyecto

Desarrollar un **API de calculadora de matrices basada en Python** que exponga operaciones matriciales a través de endpoints HTTP. Este API será utilizada por un frontend (e.g., construido con Next.js 15) para resolver problemas de álgebra lineal relevantes para el curso MAT1187.

El backend de Python debe alojarse localmente y utilizar un framework de API moderno (e.g., FastAPI o Flask). No se permiten bibliotecas matemáticas externas (como NumPy o SymPy) — solo se permiten operaciones nativas de Python.

---

## 🔧 Características y Operaciones Centrales

### 🟦 Restricciones de Tamaño de Matriz

- Todas las operaciones deben soportar **matrices cuadradas de hasta tamaño 4x4**
- Se permiten matrices rectangulares solo donde sea válido (e.g., en la multiplicación)

---

### ➕ Operaciones Básicas de Matrices

Los endpoints deben soportar:

- [x] Suma de Matrices (A + B)
- [x] Resta de Matrices (A - B)
- [x] Multiplicación de Matrices (A × B)

Requisitos:
- Validar compatibilidad de dimensiones
- Retornar matriz resultante
- Opcionalmente incluir el proceso paso a paso

---

### ➕ Documentación Detallada de Endpoints de Operaciones Básicas

#### 1. Suma de Matrices (`/operations/add`)

**Descripción:**
Realiza la suma de dos matrices, A y B (A + B). Los elementos de las matrices pueden ser números enteros, de punto flotante, o cadenas que representen fracciones (e.g., "1/2", "3 / 4", "-2/5"). El endpoint valida la compatibilidad de dimensiones (las matrices deben tener el mismo número de filas y columnas) y que el tamaño no exceda 4x4. La respuesta incluye la matriz resultante y los pasos detallados del cálculo.

**Método HTTP y URL:**
`POST {{base_url}}/operations/add`

**Formato de Solicitud (Cuerpo de la Solicitud):**
El cuerpo de la solicitud debe ser un objeto JSON con dos propiedades, `matrix_a` y `matrix_b`, ambas representando las matrices a sumar.

```json
{
  "matrix_a": [
    ["1", "1/2"],
    [2, "3.0"]
  ],
  "matrix_b": [
    ["1/2", "1"],
    [0, "-1/4"]
  ]
}
```

**Componentes de la Matriz de Entrada (`MatrixElement`):**
Cada elemento dentro de las listas de las matrices puede ser:
- `integer` (entero): Ejemplo: `1`, `-5`, `0`
- `float` (flotante): Ejemplo: `2.5`, `-0.75` (se convertirán internamente a fracciones)
- `string` (cadena de texto):
    - Representando un entero: `"4"`
    - Representando un flotante: `"4.0"`
    - Representando una fracción: `"1/2"`, `" 3 / 4 "`, `"-2/5"` (los espacios son permitidos)

**Formato de Respuesta (Éxito - `200 OK`):**

```json
{
  "success": true,
  "result": [
    ["3/2", "3/2"],
    [2, "11/4"]
  ],
  "steps": [
    "Inicio de la suma de matrices A y B.",
    "Matriz A (2x2):",
    "  |   1  1/2 |",
    "  |   2    3 |",
    "Matriz B (2x2):",
    "  | 1/2    1 |",
    "  |   0 -1/4 |",
    "Calculando cada elemento de la matriz resultante C = A + B:",
    "  C(1,1) = A(1,1) + B(1,1) = 1 + 1/2 = 3/2",
    "  C(1,2) = A(1,2) + B(1,2) = 1/2 + 1 = 3/2",
    "  C(2,1) = A(2,1) + B(2,1) = 2 + 0 = 2",
    "  C(2,2) = A(2,2) + B(2,2) = 3 + -1/4 = 11/4",
    "Suma completada."
  ],
  "error": null
}
```
**Componentes de la Matriz de Salida (`OutputElement`):**
Los elementos en la matriz `result` serán:
- `integer` (entero): Si el resultado del elemento es un número entero.
- `string` (cadena de texto): Si el resultado del elemento es una fracción (formato "num/den").

**Formato de Respuesta (Error):**
Si ocurre un error de validación o durante el procesamiento, `success` será `false` y el campo `error` contendrá un mensaje descriptivo. El código de estado HTTP será `200 OK` para errores de validación personalizados y `422 Unprocessable Entity` (Entidad no procesable) para errores de validación de Pydantic (estructura de entrada incorrecta).

*Ejemplo de Error de Dimensiones (Validación Personalizada - `200 OK`):*
```json
{
  "success": false,
  "result": null,
  "steps": null,
  "error": "Las matrices A y B deben tener el mismo número de filas para la suma/resta. A tiene 2 filas y B tiene 1 filas."
}
```

*Ejemplo de Error de Elemento Inválido (Validación Personalizada - `200 OK`):*
```json
{
  "success": false,
  "result": null,
  "steps": null,
  "error": "Valor de fracción inválido: '1/2a'. Contiene caracteres no permitidos o múltiples '/'. Use formato como 'num/den' o 'num'."
}
```

*Ejemplo de Error de Estructura (Validación Pydantic - `422 Unprocessable Entity`):*
Solicitud: `{"matrix_a": "no_es_una_matriz", "matrix_b": [[1]]}`
Respuesta:
```json
{
  "detail": [
    {
      "type": "list_of_list_type",
      "loc": [
        "body",
        "matrix_a"
      ],
      "msg": "Input should be a valid list of lists", // Mensaje original de Pydantic, puede permanecer en inglés o ser manejado para mostrarse en español.
      // ... más detalles de Pydantic ...
    }
  ]
}
```

**Casos de Prueba Comunes:**

1.  **Suma Exitosa (Enteros):**
    *   `matrix_a`: `[[1,2],[3,4]]`
    *   `matrix_b`: `[[5,6],[7,8]]`
    *   `result`: `[[6,8],[10,12]]`
2.  **Suma Exitosa (Fracciones y Mixtos):**
    *   `matrix_a`: `[["1/2", 1], [0, "0.5"]]`
    *   `matrix_b`: `[["1/2", "1/4"], [1, "3/4"]]`
    *   `result`: `[[1, "5/4"], [1, "5/4"]]`
3.  **Error: Dimensiones Incompatibles (Filas):**
    *   `matrix_a`: `[[1],[2]]`
    *   `matrix_b`: `[[1]]`
    *   `error`: `"Las matrices A y B deben tener el mismo número de filas para la suma/resta..."`
4.  **Error: Dimensiones Incompatibles (Columnas):**
    *   `matrix_a`: `[[1,2]]`
    *   `matrix_b`: `[[1]]`
    *   `error`: `"Las matrices A y B deben tener el mismo número de columnas para la suma/resta..."`
5.  **Error: Matriz Vacía:**
    *   `matrix_a`: `[]`
    *   `matrix_b`: `[[1]]`
    *   `error`: `"La matriz A no puede estar vacía."`
6.  **Error: Elemento de Matriz Inválido (Formato de Fracción):**
    *   `matrix_a`: `[["1/0"]]` (División por cero)
    *   `matrix_b`: `[["1"]]`
    *   `error`: `"Valor inválido: '1/0'. El denominador no puede ser cero en una fracción."`
7.  **Error: Límite de Tamaño Excedido (Filas > 4):**
    *   `matrix_a`: `[[1],[2],[3],[4],[5]]`
    *   `matrix_b`: `[[1],[2],[3],[4],[5]]`
    *   `error`: `"La operación está limitada a matrices de hasta 4 filas..."`

#### 2. Resta de Matrices (`/operations/subtract`)

**Descripción:**
Realiza la resta de dos matrices, A y B (A - B). Similar a la suma, los elementos pueden ser números enteros, de punto flotante, o cadenas que representen fracciones. Valida compatibilidad de dimensiones (deben ser idénticas) y el límite de tamaño (4x4). La respuesta incluye la matriz resultante y los pasos detallados.

**Método HTTP y URL:**
`POST {{base_url}}/operations/subtract`

**Formato de Solicitud (Cuerpo de la Solicitud):**
Idéntico al endpoint de suma.
```json
{
  "matrix_a": [
    ["5/2", "2"],
    [3, "1/1"]
  ],
  "matrix_b": [
    ["1/2", "1"],
    [1, "3/4"]
  ]
}
```

**Componentes de la Matriz de Entrada (`MatrixElement`):**
Igual que para la suma.

**Formato de Respuesta (Éxito - `200 OK`):**
```json
{
  "success": true,
  "result": [
    [2, 1],
    [2, "1/4"]
  ],
  "steps": [
    "Inicio de la resta de matrices A - B.",
    "Matriz A (2x2):",
    "  | 5/2  2 |",
    "  |   3  1 |",
    "Matriz B (2x2):",
    "  | 1/2  1 |",
    "  |   1  3/4 |",
    "Calculando cada elemento de la matriz resultante C = A - B:",
    "  C(1,1) = A(1,1) - B(1,1) = 5/2 - 1/2 = 2",
    "  C(1,2) = A(1,2) - B(1,2) = 2 - 1 = 1",
    "  C(2,1) = A(2,1) - B(2,1) = 3 - 1 = 2",
    "  C(2,2) = A(2,2) - B(2,2) = 1 - 3/4 = 1/4",
    "Resta completada."
  ],
  "error": null
}
```
**Componentes de la Matriz de Salida (`OutputElement`):**
Igual que para la suma.

**Formato de Respuesta (Error):**
Análogo al endpoint de suma, con mensajes de error adaptados si es necesario (aunque la mayoría de las validaciones son compartidas y producen los mismos mensajes).

**Casos de Prueba Comunes:**

1.  **Resta Exitosa (Enteros):**
    *   `matrix_a`: `[[5,8],[10,12]]`
    *   `matrix_b`: `[[1,2],[3,4]]`
    *   `result`: `[[4,6],[7,8]]`
2.  **Resta Exitosa (Fracciones y Mixtos):**
    *   `matrix_a`: `[[1, "3/4"], ["1/2", 2]]`
    *   `matrix_b`: `[["1/2", "1/4"], [0, "1.0"]]`
    *   `result`: `[["1/2", "1/2"], ["1/2", 1]]`
3.  Los casos de error (Dimensiones Incompatibles, Matriz Vacía, Elemento Inválido, Límite de Tamaño) son idénticos a los de la suma, ya que la lógica de validación subyacente es la misma.

#### 3. Multiplicación de Matrices (`/operations/multiply`)

**Descripción:**
Realiza la multiplicación de dos matrices, A y B (A × B). Los elementos de las matrices pueden ser números enteros, de punto flotante, o cadenas que representen fracciones (e.g., "1/2", "3 / 4", "-2/5"). El endpoint valida la compatibilidad de dimensiones (el número de columnas de A debe ser igual al número de filas de B) y que el tamaño de cada matriz no exceda 4x4. La respuesta incluye la matriz resultante y los pasos detallados del cálculo.

**Método HTTP y URL:**
`POST {{base_url}}/operations/multiply`

**Formato de Solicitud (Cuerpo de la Solicitud):**
El cuerpo de la solicitud debe ser un objeto JSON con dos propiedades, `matrix_a` y `matrix_b`.
```json
{
  "matrix_a": [
    ["1", "2"],
    ["3", "4"]
  ],
  "matrix_b": [
    ["2", "0"],
    ["1", "2"]
  ]
}
```

**Componentes de la Matriz de Entrada (`MatrixElement`):**
Igual que para la suma/resta.

**Formato de Respuesta (Éxito - `200 OK`):**
```json
{
  "success": true,
  "result": [
    ["4", "4"],
    ["10", "8"]
  ],
  "steps": [
    "Matriz A ingresada:",
    "Matriz A (2x2):",
    "  | 1  2 |",
    "  | 3  4 |",
    "Matriz B ingresada:",
    "Matriz B (2x2):",
    "  | 2  0 |",
    "  | 1  2 |",
    "Proceso de multiplicación (A x B):",
    "Elemento C[1][1] = (1 * 2) + (2 * 1) = 4",
    "Elemento C[1][2] = (1 * 0) + (2 * 2) = 4",
    "Elemento C[2][1] = (3 * 2) + (4 * 1) = 10",
    "Elemento C[2][2] = (3 * 0) + (4 * 2) = 8",
    "Matriz Resultante (C = A x B):",
    "Matriz Resultante C (2x2):",
    "  |  4   4 |",
    "  | 10   8 |"
  ],
  "error": null
}
```

**Componentes de la Matriz de Salida (`OutputElement`):**
Igual que para la suma/resta.

**Formato de Respuesta (Error):**
Análogo a los otros endpoints básicos. Errores de validación de Pydantic devuelven `422` (Entidad no procesable). Errores de validación personalizados (dimensiones, contenido) devuelven `200 OK` con `success: false`.

*Ejemplo de Error de Dimensiones para Multiplicación (Validación Personalizada - `200 OK`):*
```json
{
  "success": false,
  "result": null,
  "steps": null,
  "error": "Para la multiplicación, el número de columnas de la matriz A (2) debe ser igual al número de filas de la matriz B (3)."
}
```

**Casos de Prueba Comunes:**
1.  **Multiplicación Exitosa (2x2 * 2x2):**
    *   `matrix_a`: `[[1,2],[3,4]]`, `matrix_b`: `[[2,0],[1,2]]`
    *   `result`: `[[4,4],[10,8]]`
2.  **Multiplicación Exitosa (2x3 * 3x2):**
    *   `matrix_a`: `[[1,2,3],[4,5,6]]`, `matrix_b`: `[[7,8],[9,10],[11,12]]`
    *   `result`: `[[58,64],[139,154]]`
3.  **Error: Dimensiones Incompatibles:**
    *   `matrix_a`: `[[1,2],[3,4]]` (2x2)
    *   `matrix_b`: `[[1,2,3],[4,5,6],[7,8,9]]` (3x3)
    *   `error`: `"Para la multiplicación, el número de columnas de la matriz A (2) debe ser igual al número de filas de la matriz B (3)."`
4.  Errores comunes de `validar_matriz` (matriz vacía, elemento inválido, formato de fracción, límite de tamaño 4x4) aplican igual que para suma/resta.

---

### 🧮 Determinante e Inversa

Los endpoints deben soportar:

- [x] Cálculo de Determinante (hasta 4x4, método de reducción de filas)
- [x] Inversión de Matrices (hasta 4x4, método de Gauss-Jordan)

Requisitos:
- Validar que la matriz sea cuadrada.
- Retornar el valor del determinante o la matriz inversa.
- Manejar errores para matrices singulares (determinante cero).
- Opcionalmente incluir el proceso paso a paso.

---

### ➕ Documentación Detallada de Endpoints de Determinante e Inversa

#### 4. Cálculo de Determinante (`/operations/determinant`)

**Descripción:**
Calcula el determinante de una matriz cuadrada A (hasta 4x4). Los elementos pueden ser números enteros, de punto flotante, o cadenas que representen fracciones. El método utilizado es la eliminación Gaussiana para transformar la matriz a una forma triangular superior, y luego multiplicar los elementos de la diagonal (ajustando por intercambios de filas). La respuesta incluye el valor del determinante (como entero o fracción en formato cadena de texto) y los pasos detallados del cálculo.

**Método HTTP y URL:**
`POST {{base_url}}/operations/determinant`

**Formato de Solicitud (Cuerpo de la Solicitud):**
El cuerpo de la solicitud debe ser un objeto JSON con una propiedad `matrix`.
```json
{
  "matrix": [
    ["4", "7"],
    ["2", "6"]
  ]
}
```

**Componentes de la Matriz de Entrada (`MatrixElement`):**
Igual que para las operaciones básicas (suma, resta, multiplicación).

**Formato de Respuesta (Éxito - `200 OK`):**
```json
{
  "success": true,
  "result": "10", // Puede ser un entero o una fracción como "5/2"
  "steps": [
    "Matriz de entrada A:",
    "Matriz A (2x2):",
    "  | 4  7 |",
    "  | 2  6 |",
    "Transformando la matriz a forma triangular superior mediante eliminación Gaussiana:",
    "Pivote actual A(1,1) = 4",
    "Eliminando elemento A(2,1) usando la operación: F2 = F2 - (1/2) * F1",
    "Matriz después de la operación",
    "  | 4    7 |",
    "  | 0  5/2 |",
    "Pivote actual A(2,2) = 5/2",
    "La matriz está en forma triangular superior.",
    "Matriz triangular superior final",
    "  | 4    7 |",
    "  | 0  5/2 |",
    "Calculando el determinante como el producto de los elementos de la diagonal multiplicados por el factor de intercambio de filas (1):",
    "  det(A) = 1 * (4 * 5/2)",
    "         = 1 * 10",
    "         = 10",
    "El determinante final (calculado mediante eliminación Gaussiana) de la matriz A es: 10"
  ],
  "error": null
}
```

**Componentes de Salida (`result`):**
El campo `result` será:
- `string` (cadena de texto): Representando el valor del determinante, ya sea como un entero (e.g., `"10"`) o una fracción (e.g., `"5/2"`, `"-1/3"`).

**Formato de Respuesta (Error):**
Errores de validación de Pydantic devuelven `422` (Entidad no procesable). Errores de validación personalizados (matriz no cuadrada, contenido, etc.) devuelven `200 OK` con `success: false`.

*Ejemplo de Error de Matriz no Cuadrada (Validación Personalizada - `200 OK`):*
```json
{
  "success": false,
  "result": null,
  "steps": null,
  "error": "La matriz debe ser cuadrada para calcular el determinante. Se recibió una matriz de 2x3."
}
```

**Casos de Prueba Comunes:**
1.  **Determinante Exitoso (2x2):**
    *   `matrix`: `[["4","7"],["2","6"]]`
    *   `result`: `"10"`
2.  **Determinante Exitoso (3x3, con fracciones):**
    *   `matrix`: `[["1","1/2","0"],["2","1","1/3"],["0","-1/4","1"]]`
    *   `result`: `"7/12"` (o el valor que corresponda)
3.  **Determinante Cero (Matriz Singular):**
    *   `matrix`: `[["1","2"],["2","4"]]`
    *   `result`: `"0"`
4.  **Error: Matriz no Cuadrada:**
    *   `matrix`: `[["1","2","3"],["4","5","6"]]`
    *   `error`: `"La matriz debe ser cuadrada para calcular el determinante. Se recibió una matriz de 2x3."`
5.  Errores comunes de `validar_matriz` (matriz vacía, elemento inválido, formato de fracción, límite de tamaño 4x4) aplican.

#### 5. Inversión de Matrices (`/operations/inverse`)

**Descripción:**
Calcula la inversa de una matriz cuadrada A (hasta 4x4) utilizando el método de eliminación de Gauss-Jordan. Los elementos pueden ser números enteros, de punto flotante, o cadenas que representen fracciones. Si la matriz es singular (no invertible), el endpoint lo indicará. La respuesta incluye la matriz inversa (si existe) y los pasos detallados del proceso.

**Método HTTP y URL:**
`POST {{base_url}}/operations/inverse`

**Formato de Solicitud (Cuerpo de la Solicitud):**
El cuerpo de la solicitud debe ser un objeto JSON con una propiedad `matrix`.
```json
{
  "matrix": [
    ["4", "7"],
    ["2", "6"]
  ]
}
```

**Componentes de la Matriz de Entrada (`MatrixElement`):**
Igual que para las operaciones básicas.

**Formato de Respuesta (Éxito - Matriz Invertible - `200 OK`):**
```json
{
  "success": true,
  "result": [
    ["3/5", "-7/10"],
    ["-1/5", "2/5"]
  ],
  "steps": [
    "Matriz de entrada A:",
    "Matriz A (2x2):",
    "  | 4  7 |",
    "  | 2  6 |",
    "Matriz aumentada inicial [A|I]:",
    "Aumentada (2x4)", // Traducido de "Augmented (2x4)"
    "  | 4  7  1  0 |",
    "  | 2  6  0  1 |",
    // ... (numerosos pasos de Gauss-Jordan) ...
    "Proceso de eliminación de Gauss-Jordan completado.",
    "La parte izquierda es la matriz identidad, la parte derecha es la inversa A⁻¹.",
    "Matriz Inversa A⁻¹",
    "  |  3/5  -7/10 |",
    "  | -1/5    2/5 |",
    "La inversa de la matriz A ha sido calculada exitosamente."
  ],
  "error": null
}
```

**Formato de Respuesta (Éxito - Matriz Singular - `200 OK`):**
```json
{
  "success": false,
  "result": null,
  "steps": [
    "Matriz de entrada A:",
    "Matriz A (2x2):",
    "  | 1  2 |",
    "  | 2  4 |",
    "Matriz aumentada inicial [A|I]:",
    // ... (pasos hasta determinar singularidad) ...
    "No se encontró pivote no nulo en la columna 2 (después de procesar filas anteriores).",
    "La matriz no es invertible (singular)."
  ],
  "error": "La matriz no es invertible (singular). Los pasos detallan el problema."
}
```

**Componentes de la Matriz de Salida (`OutputElement`):**
Igual que para suma/resta. Si la matriz es singular, `result` será `null`.

**Formato de Respuesta (Error de Validación):**
Errores de validación de Pydantic devuelven `422` (Entidad no procesable). Errores de validación personalizados (matriz no cuadrada, contenido, etc.) devuelven `200 OK` con `success: false` y un mensaje en `error` (si no es un caso de singularidad manejado).

*Ejemplo de Error de Matriz no Cuadrada (Validación Personalizada - `200 OK`):*
```json
{
  "success": false,
  "result": null,
  "steps": null,
  "error": "La matriz debe ser cuadrada para calcular su inversa. Se recibió una matriz de 2x3."
}
```

**Casos de Prueba Comunes:**
1.  **Inversa Exitosa (2x2):**
    *   `matrix`: `[["4","7"],["2","6"]]`
    *   `result`: `[["3/5", "-7/10"], ["-1/5", "2/5"]]`
2.  **Inversa Exitosa (3x3):**
    *   `matrix`: `[["1","2","3"],[0,"1","4"],[5,"6","0"]]`
    *   `result`: `[[-24,18,5],[20,-15,-4],[-5,4,1]]`
3.  **Matriz Singular (2x2):**
    *   `matrix`: `[["1","2"],["2","4"]]`
    *   `success`: `false`, `result`: `null`, `error`: `"La matriz no es invertible (singular). Los pasos detallan el problema."`
4.  **Error: Matriz no Cuadrada:**
    *   `matrix`: `[["1","2","3"],["4","5","6"]]`
    *   `error`: `"La matriz debe ser cuadrada para calcular su inversa. Se recibió una matriz de 2x3."`
5.  Errores comunes de `validar_matriz` (matriz vacía, elemento inválido, formato de fracción, límite de tamaño 4x4) aplican.

---

### 🔁 Resolución de Sistemas de Ecuaciones Lineales

Los endpoints deben soportar:

- [x] Eliminación Gaussiana (Ax=b)
- [x] Factorización LU (A=LU)
- [x] Eliminación de Gauss-Jordan (Ax=b, forma escalonada reducida)

Requisitos:
- Aceptar la matriz de coeficientes A y el vector de constantes b.
- Validar dimensiones (A debe ser cuadrada, número de filas de A debe coincidir con el tamaño de b).
- Retornar la solución del sistema (vector x), o mensajes para casos sin solución o con soluciones infinitas.
- Opcionalmente incluir el proceso paso a paso.

---

### ➕ Documentación Detallada de Endpoints de Resolución de Sistemas

#### 6. Resolver Sistema Ax=b por Eliminación Gaussiana (`/operations/solve_system_gaussian`)

**Descripción:**
Resuelve un sistema de ecuaciones lineales de la forma Ax=b utilizando el método de Eliminación Gaussiana. El sistema debe tener una matriz de coeficientes A cuadrada (hasta 4x4) y un vector de constantes b. Los elementos de A y b pueden ser números enteros, de punto flotante o cadenas que representen fracciones. El endpoint determina si el sistema tiene una solución única, no tiene solución o tiene soluciones infinitas. La respuesta incluye el vector solución (si es única), un mensaje descriptivo del tipo de solución y los pasos detallados del proceso.

**Método HTTP y URL:**
`POST {{base_url}}/operations/solve_system_gaussian`

**Formato de Solicitud (Cuerpo de la Solicitud):**
El cuerpo de la solicitud debe ser un objeto JSON con `matrix_a` (matriz de coeficientes) y `vector_b` (vector de constantes).

```json
{
  "matrix_a": [
    [1, 1, 1],
    [0, 2, 5],
    [2, 5, -1]
  ],
  "vector_b": [6, -4, 27]
}
```

**Componentes de Entrada (`matrix_a`, `vector_b`):**
- `matrix_a`: `List[List[MatrixElement]]` (igual que para operaciones básicas).
- `vector_b`: `List[MatrixElement]` (lista de elementos, igual que los elementos de `matrix_a`).

**Formato de Respuesta (Éxito - Solución Única - `200 OK`):**
```json
{
  "success": true,
  "result": {
    "solution_vector": ["5", "3", "-2"],
    "message": "El sistema tiene una solución única."
  },
  "steps": [
    "Sistema de ecuaciones Ax=b:",
    "Matriz de coeficientes A:",
    "A (3x3):",
    "  | 1  1   1 |",
    "  | 0  2   5 |",
    "  | 2  5  -1 |",
    "Vector de constantes b:",
    "b (3x1):",
    "  |  6 |",
    "  | -4 |",
    "  | 27 |",
    "Matriz aumentada inicial [A|b]:",
    "Aumentada (3x4):",
    "  | 1  1   1 |  6 |",
    "  | 0  2   5 | -4 |",
    "  | 2  5  -1 | 27 |",
    "Intercambiando Fila 1 con Fila 3 para obtener un pivote más grande (o no nulo) en A(1,1).",
    "Matriz aumentada después del intercambio (3x4):",
    "  | 2  5  -1 | 27 |",
    "  | 0  2   5 | -4 |",
    "  | 1  1   1 |  6 |",
    "Pivote actual A(1,1) = 2",
    "Eliminando elemento A(3,1) usando la operación: F3 = F3 - (1/2) * F1",
    "Matriz aumentada después de la operación (3x4):",
    "  | 2     5   -1 |    27 |",
    "  | 0     2    5 |    -4 |",
    "  | 0  -3/2  3/2 | -15/2 |",
    "Pivote actual A(2,2) = 2",
    "Eliminando elemento A(3,2) usando la operación: F3 = F3 - (-3/4) * F2",
    "Matriz aumentada después de la operación (3x4):",
    "  | 2  5    -1 |    27 |",
    "  | 0  2     5 |    -4 |",
    "  | 0  0  21/4 | -21/2 |",
    "Pivote actual A(3,3) = 21/4",
    "Matriz en forma escalonada por filas:",
    "Forma Escalonada (3x4):",
    "  | 2  5    -1 |    27 |",
    "  | 0  2     5 |    -4 |",
    "  | 0  0  21/4 | -21/2 |",
    "Iniciando sustitución hacia atrás para encontrar la solución:",
    "  De Fila 3: 21/4*z = -21/2",
    "  z = -21/2 / 21/4 = -2",
    "  De Fila 2: 2*y + ... = -4",
    "  2*y = -4 - (-10) = 6",
    "  y = 6 / 2 = 3",
    "  De Fila 1: 2*x + ... = 27",
    "  2*x = 27 - (17) = 10",
    "  x = 10 / 2 = 5",
    "Sustitución hacia atrás completada.",
    "Solución del sistema x:",
    "x (3x1):",
    "  |  5 |",
    "  |  3 |",
    "  | -2 |"
  ],
  "error": null
}
```

**Formato de Respuesta (Éxito - Sin Solución - `200 OK`):**
```json
{
  "success": true,
  "result": {
    "message": "El sistema no tiene solución (es inconsistente)."
  },
  "steps": [
    "Sistema de ecuaciones Ax=b:",
    "Matriz de coeficientes A:",
    "A (2x2):",
    "  | 1  1 |",
    "  | 1  1 |",
    "Vector de constantes b:",
    "b (2x1):",
    "  | 2 |",
    "  | 3 |",
    "Matriz aumentada inicial [A|b]:",
    "Aumentada (2x3):",
    "  | 1  1 | 2 |",
    "  | 1  1 | 3 |",
    "Pivote actual A(1,1) = 1",
    "Eliminando elemento A(2,1) usando la operación: F2 = F2 - (1) * F1",
    "Matriz aumentada después de la operación (2x3):",
    "  | 1  1 | 2 |",
    "  | 0  0 | 1 |",
    "Matriz en forma escalonada por filas:",
    "Forma Escalonada (2x3):",
    "  | 1  1 | 2 |",
    "  | 0  0 | 1 |",
    "Fila 2 ([0...0 | 1]) indica que el sistema es inconsistente."
  ],
  "error": "El sistema no tiene solución (es inconsistente)."
}
```

**Formato de Respuesta (Éxito - Soluciones Infinitas - `200 OK`):**
```json
{
  "success": true,
  "result": {
    "message": "El sistema tiene soluciones infinitas."
  },
  "steps": [
    "Sistema de ecuaciones Ax=b:",
    "Matriz de coeficientes A:",
    "A (2x2):",
    "  | 1  1 |",
    "  | 2  2 |",
    "Vector de constantes b:",
    "b (2x1):",
    "  | 2 |",
    "  | 4 |",
    "Matriz aumentada inicial [A|b]:",
    "Aumentada (2x3):",
    "  | 1  1 | 2 |",
    "  | 2  2 | 4 |",
    "Pivote actual A(1,1) = 1",
    "Eliminando elemento A(2,1) usando la operación: F2 = F2 - (2) * F1",
    "Matriz aumentada después de la operación (2x3):",
    "  | 1  1 | 2 |",
    "  | 0  0 | 0 |",
    "Matriz en forma escalonada por filas:",
    "Forma Escalonada (2x3):",
    "  | 1  1 | 2 |",
    "  | 0  0 | 0 |",
    "El rango de la matriz de coeficientes (1) es menor que el número de variables (2).",
    "El sistema tiene soluciones infinitas (si es consistente)."
  ],
  "error": null
}
```

**Formato de Respuesta (Error - `400 Bad Request` o `200 OK` con `success: false`):**
Los errores de validación de entrada (dimensiones incompatibles, A no cuadrada, elementos inválidos, etc.) producirán una respuesta con `success: false` y un código HTTP `400 Bad Request` si es una `HTTPException` directa, o `200 OK` si es un error de validación manejado que retorna la estructura `ApiResponse`. Los errores de Pydantic por formato de datos incorrecto resultarán en un `422 Unprocessable Entity`.

*Ejemplo de Error: Matriz A no cuadrada (`400 Bad Request`):*
Solicitud: `{"matrix_a": [[1,2,3],[4,5,6]], "vector_b": [1,2]}`
Respuesta:
```json
{
  "detail": "La matriz de coeficientes A debe ser cuadrada para este método simplificado de solución única."
}
```

*Ejemplo de Error: Incompatibilidad de filas entre A y b (`400 Bad Request`):*
Solicitud: `{"matrix_a": [[1,2],[3,4]], "vector_b": [1,2,3]}`
Respuesta:
```json
{
  "detail": "El número de filas de la matriz A (2) debe coincidir con el número de elementos del vector b (3)."
}
```

*Ejemplo de Error: Elemento Inválido en Matriz A (`400 Bad Request`):*
Solicitud: `{"matrix_a": [["x"]], "vector_b": [1]}`
Respuesta:
```json
{
  "detail": "Error de conversión de valor: Valor de entrada inválido: 'x'."
}
```

**Casos de Prueba Comunes (Adicionales a los ejemplos de respuesta):**
1.  **Sistema 2x2 con Solución Única:**
    *   `matrix_a`: `[[2,1],[1,3]]`, `vector_b`: `[5,5]`
    *   `result.solution_vector`: `["2", "1"]`
2.  **Error: Matriz A Vacía (`400 Bad Request`):**
    *   `matrix_a`: `[]`, `vector_b`: `[]`
    *   `detail`: `"Error en Matriz A: A no puede estar vacía."`
3.  **Error: Vector b Vacío (`400 Bad Request`):**
    *   `matrix_a`: `[[1]]`, `vector_b`: `[]`
    *   `detail`: `"Error en Vector b: El vector b no puede estar vacío."`
4.  **Error: Matriz A Excede Límite 4x4 (`400 Bad Request`):**
    *   `matrix_a`: `Matriz 5x5`, `vector_b`: `Vector de 5 elementos`
    *   `detail`: `"La matriz A está limitada a dimensiones de hasta 4x4. Se recibió 5x5."`

---

#### 7. Factorización LU de una Matriz (`/operations/lu_factorization`)

**Descripción:**
Realiza la descomposición LU de una matriz cuadrada A (hasta 4x4), de forma que A = LU. L es una matriz triangular inferior con unos en la diagonal (método Doolittle), y U es una matriz triangular superior. Los elementos de A pueden ser números enteros, de punto flotante, o cadenas que representen fracciones. La implementación actual no utiliza pivoteo. Si durante el proceso se encuentra un pivote cero que impide la continuación sin pivoteo, el endpoint lo indicará. La respuesta incluye las matrices L y U (si la descomposición es exitosa) y los pasos detallados del cálculo.

**Método HTTP y URL:**
`POST {{base_url}}/operations/lu_factorization`

**Formato de Solicitud (Cuerpo de la Solicitud):**
El cuerpo de la solicitud debe ser un objeto JSON con una propiedad `matrix` (la matriz A a descomponer).
```json
{
  "matrix": [
    ["2", "-1", "0"],
    ["-1", "2", "-1"],
    ["0", "-1", "2"]
  ]
}
```

**Componentes de la Matriz de Entrada (`MatrixElement`):**
Igual que para las operaciones básicas (suma, resta, multiplicación).

**Formato de Respuesta (Éxito - Descomposición Posible - `200 OK`):**
```json
{
  "success": true,
  "result": {
    "matrix_l": [
      ["1", "0", "0"],
      ["-1/2", "1", "0"],
      ["0", "-2/3", "1"]
    ],
    "matrix_u": [
      ["2", "-1", "0"],
      ["0", "3/2", "-1"],
      ["0", "0", "4/3"]
    ]
  },
  "steps": [
    "Matriz de entrada A:",
    "Matriz A (3x3):",
    "  |    2  -1    0 |",
    "  |   -1   2   -1 |",
    "  |    0  -1    2 |",
    "Inicializando matrices L y U.",
    "Matriz L Inicial (3x3):",
    "  | 0  0  0 |",
    "  | 0  0  0 |",
    "  | 0  0  0 |",
    "Matriz U Inicial (3x3):",
    "  | 0  0  0 |",
    "  | 0  0  0 |",
    "  | 0  0  0 |",
    "Calculando elementos de L y U:",
    "  L(1,1) = 1 (Diagonal de L en Doolittle)",
    "  Calculando fila 1 de U:",
    "    U(1,1) = A(1,1) - Σ(L(1,p)*U(p,1)) for p=1 to 0",
    "             = 2 - 0 = 2",
    "    U(1,2) = A(1,2) - Σ(L(1,p)*U(p,2)) for p=1 to 0",
    "             = -1 - 0 = -1",
    "    U(1,3) = A(1,3) - Σ(L(1,p)*U(p,3)) for p=1 to 0",
    "             = 0 - 0 = 0",
    "  Calculando columna 1 de L (debajo de la diagonal):",
    "    L(2,1) = (A(2,1) - Σ(L(2,p)*U(p,1))) / U(1,1) for p=1 to 0",
    "             = (-1 - 0) / 2 = -1/2",
    "    L(3,1) = (A(3,1) - Σ(L(3,p)*U(p,1))) / U(1,1) for p=1 to 0",
    "             = (0 - 0) / 2 = 0",
    "  L(2,2) = 1 (Diagonal de L en Doolittle)",
    "  Calculando fila 2 de U:",
    "    U(2,2) = A(2,2) - Σ(L(2,p)*U(p,2)) for p=1 to 1",
    "             = 2 - (-1/2*-1) = 3/2",
    "    U(2,3) = A(2,3) - Σ(L(2,p)*U(p,3)) for p=1 to 1",
    "             = -1 - (-1/2*0) = -1",
    "  Calculando columna 2 de L (debajo de la diagonal):",
    "    L(3,2) = (A(3,2) - Σ(L(3,p)*U(p,2))) / U(2,2) for p=1 to 1",
    "             = (-1 - (0*-1)) / 3/2 = -2/3",
    "  L(3,3) = 1 (Diagonal de L en Doolittle)",
    "  Calculando fila 3 de U:",
    "    U(3,3) = A(3,3) - Σ(L(3,p)*U(p,3)) for p=1 to 2",
    "             = 2 - ((0*0)+(-2/3*-1)) = 4/3",
    "Descomposición LU completada.",
    "Matriz L final:",
    "L (3x3):",
    "  |    1     0    0 |",
    "  | -1/2     1    0 |",
    "  |    0  -2/3    1 |",
    "Matriz U final:",
    "U (3x3):",
    "  | 2  -1    0 |",
    "  | 0 3/2   -1 |",
    "  | 0   0  4/3 |"
  ],
  "error": null
}
```

**Formato de Respuesta (Error - Pivote Cero - `200 OK`):**
```json
{
  "success": false,
  "result": null,
  "steps": [
    "Matriz de entrada A:",
    "Matriz A (2x2):",
    "  | 0  1 |",
    "  | 2  3 |",
    // ... (pasos hasta el error)
    "Error: Pivote U(1,1) es cero. La descomposición LU (sin pivoteo) no es posible o la matriz es singular."
  ],
  "error": "Error: Pivote U(1,1) es cero. La descomposición LU (sin pivoteo) no es posible o la matriz es singular."
}
```

**Componentes de Salida (`result`):**
Si `success` es `true`, el campo `result` será un objeto con:
- `matrix_l`: `OutputMatrix` (matriz L).
- `matrix_u`: `OutputMatrix` (matriz U).
Si `success` es `false`, `result` será `null`.

**Formato de Respuesta (Error de Validación - `400 Bad Request`):**
Los errores de validación de entrada (matriz no cuadrada, elementos inválidos, etc.) producirán una `HTTPException` directa con un código HTTP `400 Bad Request`. Los errores de Pydantic por formato de datos incorrecto resultarán en un `422 Unprocessable Entity`.

*Ejemplo de Error: Matriz A no cuadrada (`400 Bad Request`):*
Solicitud: `{"matrix": [[1,2,3],[4,5,6]]}`
Respuesta:
```json
{
  "detail": "La matriz A debe ser cuadrada para la descomposición LU. Se recibió 2x3."
}
```

*Ejemplo de Error: Límite de Tamaño Excedido (`400 Bad Request`):*
Solicitud: `{"matrix": [[matriz 5x5]]}`
Respuesta:
```json
{
  "detail": "La matriz A está limitada a dimensiones de hasta 4x4 para LU. Se recibió 5x5."
}
```

**Casos de Prueba Comunes:**
1.  **Descomposición Exitosa (2x2):**
    *   `matrix`: `[["2","3"],["1","4"]]`
    *   `result.matrix_l`: `[["1","0"],["1/2","1"]]`
    *   `result.matrix_u`: `[["2","3"],["0","5/2"]]`
2.  **Descomposición Exitosa (3x3):**
    *   `matrix`: `[["1","4","3"],["2","5","4"],["1","-3","-2"]]`
    *   `result.matrix_l`: `[["1","0","0"],["2","1","0"],["1","7/3","1"]]`
    *   `result.matrix_u`: `[["1","4","3"],["0","-3","-2"],["0","0","-1/3"]]`
3.  **Error: Pivote Cero (sin pivoteo):**
    *   `matrix`: `[["0","1"],["2","3"]]`
    *   `success`: `false`, `error`: `"Error: Pivote U(1,1) es cero..."`
4.  Errores comunes de `validar_matriz` (matriz vacía, elemento inválido, formato de fracción, etc.) aplican.

---

#### 8. Resolver Sistema Ax=b por Eliminación de Gauss-Jordan (`/operations/gauss_jordan_elimination`)

**Descripción:**
Resuelve un sistema de ecuaciones lineales de la forma Ax=b utilizando el método de Eliminación de Gauss-Jordan para obtener la forma escalonada reducida por filas (RREF) de la matriz aumentada [A|b]. El sistema puede tener una matriz de coeficientes A (hasta 4x4) y un vector de constantes b. Los elementos de A y b pueden ser números enteros, de punto flotante o cadenas que representen fracciones. El endpoint determina si el sistema tiene una solución única, no tiene solución, tiene soluciones infinitas, o simplemente calcula la RREF si la matriz A no es cuadrada pero la operación es válida. La respuesta incluye el vector solución (si es única), la matriz RREF, un mensaje descriptivo del tipo de solución y los pasos detallados del proceso.

**Método HTTP y URL:**
`POST {{base_url}}/operations/gauss_jordan_elimination`

**Formato de Solicitud (Cuerpo de la Solicitud):**
El cuerpo de la solicitud debe ser un objeto JSON con `matrix_a` (matriz de coeficientes) y `vector_b` (vector de constantes).
```json
{
  "matrix_a": [
    [2, -1, 3],
    [1, 1, 1],
    [1, -1, 1]
  ],
  "vector_b": [9, 6, 2]
}
```

**Componentes de Entrada (`SystemInput`):**
- `matrix_a`: `List[List[MatrixElement]]` (matriz de coeficientes).
- `vector_b`: `List[MatrixElement]` (vector de constantes).

**Formato de Respuesta (Éxito - Solución Única - `200 OK`):**
```json
{
  "success": true,
  "result": {
    "message": "El sistema tiene una solución única.",
    "solution_vector": ["1", "2", "3"],
    "rref_matrix": [
      ["1", "0", "0", "1"],
      ["0", "1", "0", "2"],
      ["0", "0", "1", "3"]
    ]
  },
  "steps": [
    "Matriz A original:",
    "A (3x3):",
    "  |  2  -1   3 |",
    "  |  1   1   1 |",
    "  |  1  -1   1 |",
    "Vector de constantes b:",
    "b (3x1):",
    "  | 9 |",
    "  | 6 |",
    "  | 2 |",
    "Matriz aumentada inicial [A|b]:",
    "Aumentada (3x4):",
    "  |  2  -1   3 | 9 |",
    "  |  1   1   1 | 6 |",
    "  |  1  -1   1 | 2 |",
    "  Intercambiando Fila 1 con Fila 2.",
    "Después de intercambio (3x4):",
    "  | 1   1   1 | 6 |",
    "  | 2  -1   3 | 9 |",
    "  | 1  -1   1 | 2 |",
    "  Normalizando Fila 1: F1 = F1 / 1",
    "Después de normalizar (3x4):",
    "  | 1   1   1 | 6 |",
    "  | 2  -1   3 | 9 |",
    "  | 1  -1   1 | 2 |",
    "  Eliminando en Fila 2: F2 = F2 - (2) * F1",
    "Después de F2 (3x4):",
    "  |  1   1   1 |  6 |",
    "  |  0  -3   1 | -3 |",
    "  |  1  -1   1 |  2 |",
    "  Eliminando en Fila 3: F3 = F3 - (1) * F1",
    "Después de F3 (3x4):",
    "  |  1   1   1 |  6 |",
    "  |  0  -3   1 | -3 |",
    "  |  0  -2   0 | -4 |",
    "  Intercambiando Fila 2 con Fila 3.",
    "Después de intercambio (3x4):",
    "  |  1   1   1 |  6 |",
    "  |  0  -2   0 | -4 |",
    "  |  0  -3   1 | -3 |",
    "  Normalizando Fila 2: F2 = F2 / -2",
    "Después de normalizar (3x4):",
    "  | 1   1   1 | 6 |",
    "  | 0   1   0 | 2 |",
    "  | 0  -3   1 | -3 |",
    "  Eliminando en Fila 1: F1 = F1 - (1) * F2",
    "Después de F1 (3x4):",
    "  | 1  0  1 | 4 |",
    "  | 0  1  0 | 2 |",
    "  | 0 -3  1 | -3 |",
    "  Eliminando en Fila 3: F3 = F3 - (-3) * F2",
    "Después de F3 (3x4):",
    "  | 1  0  1 | 4 |",
    "  | 0  1  0 | 2 |",
    "  | 0  0  1 | 3 |",
    "  Normalizando Fila 3: F3 = F3 / 1",
    "Después de normalizar (3x4):",
    "  | 1  0  1 | 4 |",
    "  | 0  1  0 | 2 |",
    "  | 0  0  1 | 3 |",
    "  Eliminando en Fila 1: F1 = F1 - (1) * F3",
    "Después de F1 (3x4):",
    "  | 1  0  0 | 1 |",
    "  | 0  1  0 | 2 |",
    "  | 0  0  1 | 3 |",
    "Forma escalonada reducida por filas (RREF) de la matriz aumentada:",
    "RREF (3x4):",
    "  | 1  0  0 | 1 |",
    "  | 0  1  0 | 2 |",
    "  | 0  0  1 | 3 |",
    "El sistema tiene una solución única.",
    "Vector solución x:",
    "x (3x1):",
    "  | 1 |",
    "  | 2 |",
    "  | 3 |"
  ],
  "error": null
}
```

**Formato de Respuesta (Éxito - Sin Solución - `200 OK`):**
```json
{
  "success": false, // success is false as per test expectations for no solution
  "result": {
    "message": "El sistema no tiene solución (es inconsistente).",
    "solution_vector": null,
    "rref_matrix": [
      ["1", "1", "0", "0"],
      ["0", "0", "0", "1"]
    ] // Example for a 2x3 augmented matrix RREF
  },
  "steps": [
    // ... pasos hasta la detección de inconsistencia ...
    "  Fila 2 de RREF (['0', '0', '0', '1']) indica inconsistencia (0 = 1).",
    "El sistema no tiene solución (es inconsistente)."
  ],
  "error": "El sistema no tiene solución (es inconsistente)."
}
```

**Formato de Respuesta (Éxito - Soluciones Infinitas - `200 OK`):**
```json
{
  "success": true, // success is true as RREF calculation was successful
  "result": {
    "message": "El sistema tiene soluciones infinitas.",
    "solution_vector": null,
    "rref_matrix": [
      ["1", "1", "2"],
      ["0", "0", "0"]
    ] // Example for a 2x2 augmented matrix with infinite solutions
  },
  "steps": [
    // ... pasos hasta la detección de variables libres ...
    "  Hay 1 pivotes (rango de A) y 2 variables. Como (1 < 2) y el sistema es consistente.",
    "El sistema tiene soluciones infinitas."
  ],
  "error": null
}
```

**Formato de Respuesta (Éxito - RREF Calculada para No Cuadrada - `200 OK`):**
```json
{
  "success": true,
  "result": {
    "message": "Matriz en forma escalonada reducida (RREF) calculada.", // Or "El sistema tiene soluciones infinitas." if rank < num_vars
    "solution_vector": null,
    "rref_matrix": [
      ["1", "0", "-1", "-1/3"],
      ["0", "1", "2", "2/3"]
    ] // Example RREF for a 2x3 matrix A in [A|b]
  },
  "steps": [
    // ... pasos de cálculo de RREF ...
    "Forma escalonada reducida por filas (RREF) de la matriz aumentada:",
    "RREF (2x4):",
    "  | 1  0  -1  -1/3 |",
    "  | 0  1   2   2/3 |",
    "Matriz en forma escalonada reducida (RREF) calculada."
    // Or: "El sistema tiene soluciones infinitas." if applicable
  ],
  "error": null
}
```

**Formato de Respuesta (Error de Validación - `400 Bad Request` o `422 Unprocessable Entity`):**
Los errores de validación de entrada (dimensiones incompatibles, elementos inválidos, etc.) producirán una `HTTPException` directa con un código HTTP `400 Bad Request`. Los errores de Pydantic por formato de datos incorrecto resultarán en un `422 Unprocessable Entity`.

*Ejemplo de Error: Dimensiones Incompatibles A y b (`400 Bad Request`):*
```json
{
  "detail": "El número de filas de la matriz A (2) debe coincidir con el número de elementos del vector b (3)."
}
```

*Ejemplo de Error: Elemento Inválido en Matriz A (`400 Bad Request`):*
```json
{
  "detail": "Error de conversión en A[1][1]: Valor de entrada inválido: 'x'. No es un número, fracción (ej: '1/2'), ni string numérico (ej: '2.5')."
}
```

**Casos de Prueba Comunes:**
1.  **Sistema 2x2 Único:** `A=[[2,1],[1,3]]`, `b=[5,5]` -> `x=["2","1"]`
2.  **Sistema 3x3 No Solución:** `A=[[1,1,1],[0,1,1],[0,0,0]]`, `b=[1,2,3]` -> `success:false`, `error: "El sistema no tiene solución (es inconsistente)"`
3.  **Sistema 2x2 Infinitas Soluciones:** `A=[[1,1],[2,2]]`, `b=[2,4]` -> `success:true`, `message: "El sistema tiene soluciones infinitas."`
4.  **RREF de Matriz No Cuadrada (2x3 A):** `A=[[1,2,3],[4,5,6]]`, `b=[1,2]` -> `success:true`, `message: "El sistema tiene soluciones infinitas."`, RREF de `[A|b]` proporcionada.
5.  **Errores de Validación:** Matriz vacía, elementos inválidos, límites de tamaño, etc., como en otros endpoints.

---

## ⚠️ Manejo de Errores

El API debe:

- Detectar dimensiones de matriz inválidas
- Verificar división por cero
- Manejar matrices singulares o casi singulares
- Retornar mensajes de error significativos

---

## 📝 Formato de Respuesta del API

Cada endpoint debe retornar JSON en la siguiente estructura:

```json
{
  "success": true,
  "result": [[1, 0], [0, 1]], // Ejemplo: Matriz Identidad
  "steps": ["Paso 1: Intercambiar F1 y F2", "Paso 2: Eliminar debajo del pivote en F1"] // Ejemplo de pasos
}
```

---

## ✅ Resumen de Características

| Característica             | Estado |
|----------------------------|--------|
| Suma de Matrices           | ✅     |
| Resta de Matrices          | ✅     |
| Multiplicación de Matrices | ✅     |
| Cálculo de Determinante    | ✅     |
| Cálculo de Inversa         | ✅     |
| Eliminación Gaussiana      | ✅     |
| Factorización LU           | ✅     |
| Eliminación de Gauss-Jordan| ✅     |
| Manejo de Errores          | ✅     |
| Respuestas del API en JSON | ✅     |

---

## 🛠️ Notas de Implementación del Backend

- Lenguaje: Python 3
- Framework del API: FastAPI
- Alojamiento: Localhost (e.g., http://localhost:8000)
- Sin bibliotecas matemáticas externas (Python puro)


