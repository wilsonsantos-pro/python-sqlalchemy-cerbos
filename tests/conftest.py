import pytest
from fastapi.testclient import TestClient

from cerbos_example.app.api import app
from cerbos_example.database import Base, engine
from cerbos_example.example_data import example_data


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def test_data():
    Base.metadata.create_all(engine)
    example_data()
