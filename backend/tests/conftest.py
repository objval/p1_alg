import pytest
from fastapi.testclient import TestClient
from backend.main import app 

@pytest.fixture(scope="session")
def client():
    """Proporciona una instancia de TestClient para la aplicación FastAPI."""
    with TestClient(app) as c:
        yield c 