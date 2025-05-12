# Proyecto Álgebra Lineal MAT1187 - TODO

## Backend (API con FastAPI - Python)

### Configuración del Proyecto Backend
- [✅] Inicializar proyecto FastAPI.
- [✅] Estructurar carpetas y módulos del backend (`operations`, `utils`, `tests`).
- [✅] Configurar entorno de desarrollo (dependencias, `requirements.txt`).

### Operaciones Básicas de Matrices
- [✅] **Endpoint Suma de Matrices (A + B) (`/operations/add`)**
    - [✅] Implementar lógica de suma.
    - [✅] Validar compatibilidad de dimensiones.
    - [✅] Retornar matriz resultante.
    - [✅] Incluir pasos del proceso en la respuesta.
    - [✅] Documentación y docstrings en español.
- [✅] **Endpoint Resta de Matrices (A - B) (`/operations/subtract`)**
    - [✅] Implementar lógica de resta.
    - [✅] Validar compatibilidad de dimensiones.
    - [✅] Retornar matriz resultante.
    - [✅] Incluir pasos del proceso en la respuesta.
    - [✅] Documentación y docstrings en español.
- [✅] **Endpoint Multiplicación de Matrices (A × B) (`/operations/multiply`)**
    - [✅] Implementar lógica de multiplicación.
    - [✅] Validar compatibilidad de dimensiones (cuadradas y rectangulares).
    - [✅] Retornar matriz resultante.
    - [✅] Incluir pasos del proceso en la respuesta.
    - [✅] Documentación y docstrings en español.

### Determinante e Inversa
- [✅] **Endpoint Cálculo de Determinante**
    - [✅] Implementar lógica para matrices cuadradas (hasta 4x4).
    - [✅] Método: reducción de filas (Eliminación Gaussiana).
    - [✅] Retornar el valor del determinante.
    - [✅] Incluir pasos del proceso en la respuesta.
    - [✅] Documentación y docstrings en español.
- [✅] **Endpoint Inversión de Matrices**
    - [✅] Implementar lógica para matrices cuadradas (hasta 4x4).
    - [✅] Método: Gauss-Jordan o adjunta (sin bibliotecas externas).
    - [✅] Retornar matriz inversa.
    - [✅] Manejar error para matrices singulares.
    - [✅] Incluir pasos del proceso en la respuesta.
    - [✅] Documentación y docstrings en español.

### Resolución de Sistemas de Ecuaciones Lineales
- [✅] **Endpoint Eliminación Gaussiana**
    - [✅] Implementar algoritmo de Eliminación Gaussiana.
    - [✅] Retornar solución del sistema.
    - [✅] Incluir pasos intermedios del proceso en la respuesta.
    - [✅] Documentación y docstrings en español.
- [✅] **Endpoint Factorización LU**
    - [✅] Implementar descomposición A = L × U.
    - [✅] Retornar matrices L y U.
    - [✅] Incluir pasos del proceso en la respuesta.
    - [✅] Documentación y docstrings en español.
- [✅] **Endpoint Eliminación de Gauss-Jordan**
    - [✅] Implementar algoritmo de Eliminación de Gauss-Jordan (reducción completa).
    - [✅] Retornar solución del sistema.
    - [✅] Incluir pasos intermedios del proceso en la respuesta.
    - [✅] Documentación y docstrings en español.

### General API Backend
- [✅] Implementar manejo de errores robusto (dimensiones inválidas, división por cero, matrices singulares/casi singulares) con mensajes claros en español. (Implementado para Suma/Resta, Determinante, Inversa, Multiplicación)
- [✅] Asegurar que todos los endpoints acepten JSON y retornen JSON según especificación (`success`, `result`, `steps`). (Implementado para Suma/Resta, Determinante, Inversa, Multiplicación)
- [✅] Adherirse a la restricción de no usar bibliotecas matemáticas externas (NumPy, SymPy, etc.). (Cumplido hasta ahora)
- [✅] Escribir pruebas unitarias para cada operación. (Implementado para Suma/Resta, Determinante, Inversa, Multiplicación, LU)
- [✅] Documentación general del API (e.g., README para el backend).

## Frontend (Interfaz de Usuario - HTML, CSS, JavaScript)
- [✅] Estructura HTML base con pestañas para operaciones.
- [✅] Estilos CSS básicos para la calculadora.
- [✅] Funcionalidad JavaScript para:
    - [✅] Creación dinámica de campos de entrada de matriz.
    - [✅] Manejo de pestañas.
    - [✅] Llamadas a API para Suma/Resta, Multiplicación, Determinante, Inversa, Eliminación Gaussiana.
    - [✅] Visualización de resultados y pasos.
    - [✅] Manejo de errores.

