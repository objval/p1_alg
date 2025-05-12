from fractions import Fraction
from typing import Union

# Importación eliminada de MatrixElement y OutputElement ya que no se usan directamente aquí
# y causaban error si OutputElement no estaba definido en models.py
# from backend.models import MatrixElement, OutputElement 

def to_fraction(value: Union[int, float, str]) -> Fraction:
    """
    Convierte un valor de entrada (que puede ser int, float, o str representando un número o fracción)
    a un objeto Fraction.
    Maneja espacios en blanco, convierte flotantes a fracciones con denominadores limitados,
    y valida formatos de fracción.

    Raises:
        ValueError: Si el valor es inválido (e.g., "1/0", "abc", "1/2a").
    """
    if isinstance(value, Fraction):
        return value
    if isinstance(value, (int, float)):
        # Limitar el denominador para flotantes para evitar fracciones muy complejas
        return Fraction(value).limit_denominator(1000000) 
    
    if isinstance(value, str):
        value = value.strip() # Eliminar espacios al inicio/final
        if not value: # Si la cadena está vacía después de strip
            raise ValueError("El valor de entrada de la matriz no puede ser una cadena vacía.")
        
        # Comprobar caracteres no permitidos (excepto dígitos, '/', '-', '.', y espacio)
        # El espacio ya se manejó con strip() para los extremos, pero puede estar en medio de una fracción como "1 / 2"
        allowed_chars = set("0123456789/-. ") 
        if not all(char in allowed_chars for char in value):
            # This matches the expected error in several tests for non-numeric/non-fraction characters
            raise ValueError(f"Valor de entrada inválido: '{value}'. No es un número, fracción (ej: '1/2'), ni string numérico (ej: '2.5').")

        # Manejar la conversión de string a fracción
        if '/' in value:
            parts = value.split('/')
            if len(parts) != 2:
                raise ValueError(f"Valor de fracción inválido: '{value}'. Formato debe ser num/den.")
            
            num_str, den_str = parts[0].strip(), parts[1].strip()
            
            # Intentar convertir numerador y denominador, que podrían ser flotantes o enteros
            try:
                # Convertir a float primero para manejar "1.0" o "2.5" como parte de una fracción,
                # luego a Fraction para que maneje la simplificación si es necesario.
                num = Fraction(float(num_str)) if '.' in num_str else Fraction(int(num_str))
                den = Fraction(float(den_str)) if '.' in den_str else Fraction(int(den_str))
            except ValueError:
                raise ValueError(f"Numerador o denominador inválido en la fracción: '{value}'. Deben ser numéricos.")
            
            if den == 0:
                raise ValueError(f"Valor inválido: '{value}'. El denominador no puede ser cero en una fracción.")
            return num / den
        else:
            # Intentar convertir como flotante si hay '.', sino como entero
            try:
                if '.' in value:
                    return Fraction(float(value)).limit_denominator(1000000)
                else:
                    return Fraction(int(value))
            except ValueError:
                raise ValueError(f"Valor numérico inválido: '{value}'. No es un entero, flotante o fracción válida.")
    
    raise ValueError(f"Tipo de valor no soportado: {type(value)}. Debe ser int, float, o str.")

def format_fraction_output(value: Fraction) -> str:
    """
    Formatea un objeto Fraction para la salida JSON.
    Si el denominador es 1, retorna solo el numerador como string.
    De lo contrario, retorna la fracción como "numerador/denominador".
    """
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}" 