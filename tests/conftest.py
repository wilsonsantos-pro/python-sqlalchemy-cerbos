import pytest
from fastapi.testclient import TestClient

from cerbos_example.app.api import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)
