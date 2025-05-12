from typing import List
from backend.models import OutputMatrix 

def format_matrix_for_steps(matrix_data: OutputMatrix, name: str) -> List[str]:
    if not matrix_data: 
        return [f"{name} (0x0): []"]
    if not isinstance(matrix_data[0], list):
        return [f"{name}: (datos de fila inválidos)"]

    num_filas = len(matrix_data)
    if num_filas == 0: 
        return [f"{name} (0x0): []"]
    
    num_columnas = 0
    if num_filas > 0 and isinstance(matrix_data[0], list):
        num_columnas = len(matrix_data[0])

    header = [f"{name} ({num_filas}x{num_columnas}):"]
    if num_columnas == 0: 
        return header + ["  | |" for _ in range(num_filas)]

    str_matrix = [[str(el) for el in row] for row in matrix_data]
    max_widths = [0] * num_columnas
    for row in str_matrix:
        for i, item in enumerate(row):
            if len(item) > max_widths[i]:
                max_widths[i] = len(item)

    formatted_rows = []
    for row in str_matrix:
        formatted_row_content = ""
        for i, item in enumerate(row):
            formatted_row_content += item.rjust(max_widths[i] if i < len(max_widths) else 0) + "  " 
        formatted_rows.append(f"  | {formatted_row_content.rstrip()} |")
    return header + formatted_rows 

def format_augmented_matrix_for_steps(augmented_matrix_data: OutputMatrix, main_matrix_cols: int, name: str) -> List[str]:
    """
    Formatea una matriz aumentada [A|b] o [A|I] para mostrarla en los pasos,
    con un separador visual antes de la parte aumentada.
    main_matrix_cols: número de columnas de la matriz original A.
    """
    if not augmented_matrix_data:
        return [f"{name} (0x0): []"]
    if not isinstance(augmented_matrix_data[0], list):
        return [f"{name}: (datos de fila inválidos)"]

    num_filas = len(augmented_matrix_data)
    if num_filas == 0:
        return [f"{name} (0x0): []"]
    
    total_cols = 0
    if num_filas > 0 and isinstance(augmented_matrix_data[0], list):
        total_cols = len(augmented_matrix_data[0])

    header = [f"{name} ({num_filas}x{total_cols}):"]
    if total_cols == 0:
        return header + ["  | |" for _ in range(num_filas)]
    if main_matrix_cols < 0 or main_matrix_cols > total_cols:
        return header + ["  Error: main_matrix_cols inválido para el separador."]

    str_matrix = [[str(el) for el in row] for row in augmented_matrix_data]
    max_widths = [0] * total_cols
    for row in str_matrix:
        for i, item in enumerate(row):
            if len(item) > max_widths[i]:
                max_widths[i] = len(item)

    formatted_rows = []
    for row in str_matrix:
        formatted_row_parts = []
        for i, item in enumerate(row):
            formatted_row_parts.append(item.rjust(max_widths[i] if i < len(max_widths) else 0))
        
        # Insertar separador
        if main_matrix_cols > 0 and main_matrix_cols < total_cols:
            # El separador va DESPUÉS de la columna (main_matrix_cols - 1) en índice base 0
            # y ANTES de la columna main_matrix_cols
            left_part = "  ".join(formatted_row_parts[:main_matrix_cols])
            right_part = "  ".join(formatted_row_parts[main_matrix_cols:])
            formatted_rows.append(f"  | {left_part} | {right_part} |")
        else: # No hay parte aumentada o es toda la matriz
            formatted_rows.append(f"  | {"  ".join(formatted_row_parts)} |")
            
    return header + formatted_rows 