import uuid
from unittest.mock import ANY, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_driver


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


def test_create_person(client):
    mock_driver, mock_session = mock_neo4j_driver_with_session()
    app.dependency_overrides[get_driver] = lambda: mock_driver

    response = client.post("/people", json={"name": "Alice"})
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Alice"
    assert isinstance(data["uid"], str)
    assert str(uuid.UUID(data["uid"])) == data["uid"]

    mock_session.run.assert_called_once_with(
        "CREATE (p:Person {uid: $uid, name: $name})", uid=ANY, name="Alice"
    )


def test_get_person_found(client):
    person = {"uid": "123", "name": "Alice"}
    mock_driver, _ = mock_neo4j_driver_with_session(single_record={"p": person})
    app.dependency_overrides[get_driver] = lambda: mock_driver

    response = client.get("/people/123")
    assert response.status_code == 200
    assert response.json() == person


def test_get_person_not_found(client):
    mock_driver, _ = mock_neo4j_driver_with_session(single_record=None)
    app.dependency_overrides[get_driver] = lambda: mock_driver

    response = client.get("/people/does-not-exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Person not found"


def mock_neo4j_driver_with_session(mock_records=None, single_record=None):
    mock_session = MagicMock()
    mock_session.run.return_value = MagicMock(
        __iter__=lambda self: iter(mock_records or []),
        single=MagicMock(return_value=single_record),
    )
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    return mock_driver, mock_session
