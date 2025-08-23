import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(autouse=True)
def reset_dependency_overrides():
    yield
    app.dependency_overrides = {}


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
