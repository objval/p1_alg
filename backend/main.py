from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import HTMLResponse 
from starlette.staticfiles import StaticFiles 
from fastapi.middleware.cors import CORSMiddleware
from backend.models import ApiResponse, MatrixInput, TwoMatrixInput 
from backend.operations.addition import router as addition_router
from backend.operations.subtraction import router as subtraction_router
from backend.operations.multiplication import router as multiplication_router
from backend.operations.determinant import router as determinant_router
from backend.operations.inverse import router as inverse_router # Router para matriz inversa
from backend.operations.gaussian_elimination import router as gaussian_elimination_router # Router para eliminación Gaussiana
from backend.operations.lu_factorization import router as lu_factorization_router # Router para factorización LU
from backend.operations.gauss_jordan_elimination import router as gauss_jordan_elimination_router # Router para eliminación Gauss-Jordan
import pathlib 

app = FastAPI(
    title="Calculadora de Álgebra Lineal MAT1187",
    description="API para realizar operaciones matriciales para el curso MAT1187. Implementada con FastAPI en Python.",
    version="0.1.0",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes, ajustar para producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todas las cabeceras
)

# --- Determinar la ruta absoluta al directorio 'static' ---
STATIC_DIR = pathlib.Path(__file__).resolve().parent / "static"
INDEX_HTML_PATH = STATIC_DIR / "index.html"

# Incluir routers para todas las operaciones matriciales
app.include_router(addition_router, prefix="/operations", tags=["Matrix Operations"]) 
app.include_router(subtraction_router, prefix="/operations", tags=["Matrix Operations"])
app.include_router(multiplication_router, prefix="/operations", tags=["Matrix Operations"])
app.include_router(determinant_router, prefix="/operations", tags=["Matrix Operations"]) 
app.include_router(inverse_router, prefix="/operations", tags=["Matrix Operations"]) 
app.include_router(gaussian_elimination_router, prefix="/operations", tags=["Matrix Operations"])
app.include_router(lu_factorization_router, prefix="/operations", tags=["Matrix Operations"])
app.include_router(gauss_jordan_elimination_router, prefix="/operations", tags=["Matrix Operations"])

# Montar los archivos estáticos para la interfaz de usuario
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root():
    """
    Sirve la página principal de la aplicación (index.html).
    
    Returns:
        HTMLResponse: Contenido HTML de la página principal o página de error si no se encuentra.
    """
    try:
        with open(INDEX_HTML_PATH, encoding="utf-8") as f: # Usar ruta absoluta
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<html><body><h1>Archivo no encontrado</h1><p>index.html no encontrado.</p></body></html>", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"<html><body><h1>Error</h1><p>Ocurrió un error: {str(e)}</p></body></html>", status_code=500)


@app.get("/health", summary="Chequeo de salud del API", tags=["General"])
async def health_check():
    """
    Endpoint para verificar el estado de la API.
    
    Returns:
        dict: Estado de la API con clave "status" y valor "ok".
    """
    return {"status": "ok"}

if __name__ == "__main__":
    # Para ejecutar la API localmente (opcional, uvicorn puede manejar esto desde la terminal):
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)