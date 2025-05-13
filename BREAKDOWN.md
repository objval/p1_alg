# Desglose Matemático de las Operaciones

Este documento detalla los conceptos y métodos matemáticos implementados en cada módulo del directorio `backend/operations`.

## 1. Suma de Matrices (`addition.py`)

### Concepto Matemático
La suma de dos matrices A y B de las mismas dimensiones (m x n) resulta en una matriz C, también de dimensiones m x n, donde cada elemento C<sub>ij</sub> es la suma de los elementos correspondientes A<sub>ij</sub> y B<sub>ij</sub>.
$$ C_{ij} = A_{ij} + B_{ij} $$

### Implementación y Método
- **Método:** Suma directa elemento a elemento.
- **Código:** Itera sobre cada fila `i` y columna `j` de las matrices de entrada (previamente convertidas a `Fraction` para manejar enteros y fracciones). Calcula `A[i][j] + B[i][j]` y almacena el resultado en `C[i][j]`.
- **Validación:** Verifica que ambas matrices tengan exactamente las mismas dimensiones.

## 2. Resta de Matrices (`subtraction.py`)

### Concepto Matemático
Similar a la suma, la resta de dos matrices A y B de las mismas dimensiones (m x n) produce una matriz C (m x n), donde cada elemento C<sub>ij</sub> es la diferencia de los elementos correspondientes A<sub>ij</sub> y B<sub>ij</sub>.
$$ C_{ij} = A_{ij} - B_{ij} $$

### Implementación y Método
- **Método:** Resta directa elemento a elemento.
- **Código:** Es análogo al de la suma. Itera sobre filas y columnas, calcula `A[i][j] - B[i][j]` (usando `Fraction`) y lo guarda en `C[i][j]`.
- **Validación:** Requiere que ambas matrices tengan las mismas dimensiones.

## 3. Multiplicación de Matrices (`multiplication.py`)

### Concepto Matemático
La multiplicación de una matriz A de dimensiones m x n por una matriz B de dimensiones n x p resulta en una matriz C de dimensiones m x p. Cada elemento C<sub>ij</sub> se calcula como el producto punto de la fila `i` de A y la columna `j` de B.
$$ C_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj} $$

### Implementación y Método
- **Método:** Producto punto estándar.
- **Código:** Utiliza tres bucles anidados:
    - Bucle externo para las filas `i` de A (y C).
    - Bucle intermedio para las columnas `j` de B (y C).
    - Bucle interno para el índice `k` que recorre las columnas de A y las filas de B.
- Dentro del bucle interno, calcula `A[i][k] * B[k][j]` y lo acumula en `C[i][j]`. Se usan `Fraction` para los cálculos.
- **Validación:** Verifica que el número de columnas de A sea igual al número de filas de B.

## 4. Determinante (`determinant.py`)

### Concepto Matemático
El determinante es un valor escalar asociado a una matriz cuadrada. Proporciona información sobre las propiedades de la matriz y la transformación lineal que representa (ej., si es invertible, factor de escala de volumen).

### Implementación y Método
- **Método:** Eliminación Gaussiana.
- **Código:**
    1. Transforma la matriz de entrada A en una matriz triangular superior U mediante operaciones elementales de fila (suma de filas, intercambio de filas).
    2. Lleva un registro de los intercambios de fila, ya que cada intercambio multiplica el determinante por -1.
    3. El determinante de A es el producto de los elementos de la diagonal de U, multiplicado por (-1)<sup>número de intercambios</sup>.
    4. Si durante el proceso se encuentra una columna sin pivote (todos los elementos debajo de la diagonal son cero), el determinante es 0.
- **Casos Base:** Para 1x1, det(A) = A<sub>11</sub>. Para 0x0, se considera 1 por convención (aunque el código lo evita).
- **Validación:** La matriz debe ser cuadrada.

## 5. Inversa de Matriz (`inverse.py`)

### Concepto Matemático
La inversa de una matriz cuadrada A, denotada como A<sup>-1</sup>, es aquella matriz tal que A * A<sup>-1</sup> = A<sup>-1</sup> * A = I, donde I es la matriz identidad. Una matriz es invertible si y sólo si su determinante es distinto de cero.

### Implementación y Método
- **Método:** Eliminación de Gauss-Jordan.
- **Código:**
    1. Crea una matriz aumentada [A | I], donde I es la matriz identidad de la misma dimensión que A.
    2. Aplica operaciones elementales de fila a toda la matriz aumentada para transformar la parte izquierda (A) en la matriz identidad (I).
    3. Las mismas operaciones aplicadas a la parte derecha (I) la transformarán en la matriz inversa (A<sup>-1</sup>). El resultado final es [I | A<sup>-1</sup>].
    4. Si en algún punto no se puede obtener un pivote no nulo en la parte izquierda o si la parte izquierda no se puede reducir a I, la matriz A no es invertible.
- **Validación:** La matriz debe ser cuadrada.

## 6. Eliminación Gaussiana (`gaussian_elimination.py`)

### Concepto Matemático
Es un algoritmo para resolver sistemas de ecuaciones lineales Ax = b. Transforma la matriz aumentada [A | b] a una forma escalonada por filas (REF - Row Echelon Form).

### Implementación y Método
- **Fase de Eliminación (Hacia Adelante):**
    1. Se forma la matriz aumentada [A | b].
    2. Se usan operaciones elementales de fila para introducir ceros debajo de los pivotes (el primer elemento no nulo de cada fila principal). Se puede usar pivoteo parcial (intercambiar filas para usar el pivote de mayor magnitud) para mejorar la estabilidad numérica.
    3. El objetivo es obtener una matriz triangular superior en la parte A.
- **Fase de Sustitución (Hacia Atrás):**
    1. Una vez en forma escalonada, se resuelve el sistema empezando por la última ecuación (que idealmente tendrá una sola variable) y sustituyendo los valores hacia arriba en las ecuaciones anteriores.
- **Análisis de Solución:**
    - Si se encuentra una fila [0 0 ... 0 | c] con c ≠ 0, el sistema es inconsistente (sin solución).
    - Si el rango de A (número de pivotes) es igual al número de variables, hay solución única.
    - Si el rango de A es menor que el número de variables, hay infinitas soluciones (si es consistente). (La implementación actual se enfoca en la solución única o indica los otros casos).
- **Validación:** La implementación actual asume A cuadrada para simplificar la búsqueda de solución única post-eliminación. El número de filas de A debe coincidir con el número de elementos de b.

## 7. Eliminación Gauss-Jordan (`gauss_jordan_elimination.py`)

### Concepto Matemático
Es una variación de la eliminación gaussiana que reduce la matriz aumentada [A | b] a su forma escalonada reducida por filas (RREF - Reduced Row Echelon Form).

### Implementación y Método
- **Proceso:**
    1. Similar a la eliminación gaussiana, se usa pivoteo y operaciones de fila para introducir ceros.
    2. A diferencia de la eliminación gaussiana, se introducen ceros *tanto debajo como encima* de cada pivote.
    3. Además, cada pivote se normaliza a 1 dividiendo su fila por el valor del pivote.
- **Resultado (RREF):** La matriz resultante tiene pivotes iguales a 1, y todos los demás elementos en las columnas de los pivotes son 0.
- **Análisis de Solución (desde RREF):**
    - Si hay una fila [0 0 ... 0 | 1], es inconsistente (sin solución).
    - Si no hay inconsistencia y el número de pivotes (rango) es igual al número de variables, hay solución única (los valores estarán en la columna aumentada).
    - Si no hay inconsistencia y el número de pivotes es menor que el número de variables, hay infinitas soluciones (las variables sin pivote son libres).
- **Validación:** Requiere que el número de filas de A coincida con el número de elementos de b. Funciona para matrices A no cuadradas.

## 8. Factorización LU (`lu_factorization.py`)

### Concepto Matemático
Descompone una matriz cuadrada A en el producto de dos matrices: A = LU, donde L es una matriz triangular *inferior* y U es una matriz triangular *superior*.

### Implementación y Método
- **Método:** Doolittle (sin pivoteo).
- **Condiciones de Doolittle:** L tiene unos (1) en su diagonal principal.
- **Código:**
    1. Inicializa L como identidad y U como ceros (o viceversa, adaptando las fórmulas). La implementación actual inicializa ambas con ceros y calcula los elementos.
    2. Itera sobre las filas/columnas `k` de 0 a n-1.
    3. Calcula la fila `k` de U usando:
       $$ U_{kj} = A_{kj} - \sum_{p=0}^{k-1} L_{kp} U_{pj} \quad (para \ j = k, ..., n-1) $$
    4. Calcula la columna `k` de L (debajo de la diagonal) usando:
       $$ L_{ik} = \frac{1}{U_{kk}} (A_{ik} - \sum_{p=0}^{k-1} L_{ip} U_{pk}) \quad (para \ i = k+1, ..., n-1) $$
    5. Se establece L<sub>kk</sub> = 1.
- **Fallo:** El método (sin pivoteo) falla si se encuentra un pivote U<sub>kk</sub> = 0 durante el cálculo. Esto indica que la matriz A no tiene factorización LU *sin intercambio de filas* o es singular.
- **Validación:** La matriz A debe ser cuadrada.

---

# Posibles Preguntas del Profesor y Respuestas

**P1: ¿Por qué utilizaron la biblioteca `fractions.Fraction` en lugar de números de punto flotante (floats) para los cálculos?**

*   **R:** Elegimos `fractions.Fraction` para mantener la precisión exacta en los cálculos. El álgebra lineal, especialmente en contextos académicos y al mostrar pasos intermedios, a menudo involucra fracciones que pueden perder precisión si se convierten a punto flotante. Esto es crucial para operaciones como la eliminación gaussiana, donde pequeños errores de redondeo pueden acumularse y llevar a resultados incorrectos, especialmente al determinar si un pivote es cero o al calcular inversas y determinantes de matrices mal condicionadas. Usar fracciones garantiza que los resultados sean matemáticamente exactos, tal como se harían a mano.

**P2: Para calcular el determinante, ¿por qué eligieron el método de eliminación gaussiana en lugar de, por ejemplo, la expansión por cofactores?**

*   **R:** La eliminación gaussiana (transformando a forma triangular superior y multiplicando la diagonal) es computacionalmente más eficiente para matrices de tamaño general (n > 3) que la expansión por cofactores. La complejidad de la expansión por cofactores es O(n!), mientras que la eliminación gaussiana es O(n<sup>3</sup>). Para nuestra calculadora, que soporta matrices hasta 4x4, ambas serían factibles, pero la eliminación gaussiana es un método más estándar en implementaciones numéricas y se alinea bien con otros algoritmos que ya implementamos (como la resolución de sistemas).

**P3: ¿Cuál es la diferencia fundamental entre la Eliminación Gaussiana y la Eliminación de Gauss-Jordan tal como las implementaron para resolver sistemas Ax=b? ¿Cuándo usarían una sobre la otra?**

*   **R:** La diferencia principal radica en el objetivo final de la reducción de la matriz aumentada [A|b]:
    *   **Eliminación Gaussiana:** Reduce la matriz a la *forma escalonada por filas* (REF). Esto crea una matriz triangular superior en la parte A. Luego, se requiere un paso adicional de *sustitución hacia atrás* para encontrar la solución.
    *   **Eliminación Gauss-Jordan:** Reduce la matriz a la *forma escalonada reducida por filas* (RREF). Esto crea una matriz identidad (o casi identidad, con columnas de ceros para variables libres) en la parte A. La solución (si es única) aparece directamente en la columna aumentada, eliminando la necesidad de sustitución hacia atrás.
    *   **Cuándo usar cuál:** Gauss-Jordan es conceptualmente más simple para leer la solución directamente de la RREF y es muy útil para encontrar inversas. Sin embargo, generalmente requiere más operaciones aritméticas que la eliminación gaussiana seguida de sustitución hacia atrás. Para resolver un *único* sistema Ax=b, Gaussiana + sustitución puede ser ligeramente más rápido. Para encontrar la inversa o analizar completamente la estructura de soluciones (incluyendo infinitas), Gauss-Jordan (RREF) es más directo.

**P4: La factorización LU implementada usa el método de Doolittle sin pivoteo. ¿Qué limitaciones tiene esto y cómo podrían superarse?**

*   **R:** La principal limitación de la factorización LU sin pivoteo (como Doolittle o Crout) es que falla si se encuentra un cero en la posición del pivote (U<sub>kk</sub> = 0) durante el proceso. Esto puede ocurrir incluso si la matriz es invertible. Además, pivotes muy pequeños (cercanos a cero) pueden llevar a inestabilidad numérica (grandes errores de redondeo si usáramos floats).
*   **Cómo superarlo:** La solución estándar es implementar **pivoteo parcial**. Antes de procesar la columna `k`, se busca el elemento de mayor valor absoluto en esa columna (desde la fila `k` hacia abajo). Luego, se intercambia la fila actual (`k`) con la fila que contiene ese elemento máximo. Esto asegura que el pivote U<sub>kk</sub> sea lo más grande posible (y no cero si la matriz es invertible), mejorando la estabilidad numérica y permitiendo la factorización para una clase más amplia de matrices. Registrar los intercambios de fila es necesario, lo que generalmente resulta en una factorización PA = LU, donde P es una matriz de permutación.

**P5: ¿Por qué es importante la validación de dimensiones antes de realizar operaciones como la suma, resta o multiplicación?**

*   **R:** Las operaciones matriciales están definidas matemáticamente solo para ciertas dimensiones compatibles:
    *   **Suma/Resta:** Requieren que ambas matrices tengan exactamente las *mismas dimensiones* (m x n) porque la operación se realiza elemento a elemento.
    *   **Multiplicación (A x B):** Requiere que el número de *columnas de A* sea igual al número de *filas de B* (A: m x n, B: n x p). Esto se debe a que el cálculo de cada elemento del resultado implica un producto punto entre una fila de A y una columna de B, los cuales deben tener la misma longitud (n).
*   Realizar estas validaciones *antes* de intentar los cálculos previene errores matemáticos y errores en tiempo de ejecución en el código (ej., intentar acceder a índices inexistentes). Asegura que la operación solicitada sea matemáticamente válida.

**P6: ¿Cómo maneja su implementación el caso de sistemas de ecuaciones sin solución o con infinitas soluciones en Gauss-Jordan?**

*   **R:** Nuestra implementación de Gauss-Jordan analiza la matriz RREF resultante:
    *   **Sin Solución (Inconsistente):** Detectamos si aparece una fila de la forma [0 0 ... 0 | c] donde c (en la columna aumentada) es distinto de cero. Esto representa una ecuación imposible (0 = c), indicando que el sistema no tiene solución. El código identifica esta situación y devuelve un mensaje apropiado.
    *   **Infinitas Soluciones:** Esto ocurre cuando el sistema es consistente (no hay filas [0...0|c≠0]) pero el número de pivotes (rango de A) es *menor* que el número de variables. Las columnas sin pivote corresponden a variables libres. Nuestra implementación detecta esta condición (rango < número de variables) y devuelve un mensaje indicando que existen infinitas soluciones, aunque no calcula la forma paramétrica de la solución general.
    *   **Solución Única:** Ocurre cuando el sistema es consistente y el número de pivotes es igual al número de variables. La solución se lee directamente de la columna aumentada de la RREF.
