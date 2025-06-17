import uuid
from unittest.mock import ANY, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_driver


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_dependency_overrides():
    yield
    app.dependency_overrides = {}


def mock_neo4j_driver_with_session(mock_records=None, single_record=None):
    """
    Mocks a Neo4j driver with a session, returning
    mock_records for iteration
    single_record for .single()
    """
    mock_session = MagicMock()
    mock_session.run.return_value = MagicMock(
        __iter__=lambda self: iter(mock_records or []),
        single=MagicMock(return_value=single_record),
    )
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    return mock_driver, mock_session


def test_get_all_people_empty(client):
    # arrange
    mock_driver, mock_session = mock_neo4j_driver_with_session(mock_records=[])
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.get("/people")

    # assert
    assert response.status_code == 200
    assert response.json() == []

    mock_session.run.assert_called_once_with("MATCH (p:Person) RETURN p")


def test_get_all_people(client):
    # arrange
    mock_records = [
        {"p": {"uid": "123", "name": "Alice"}},
        {"p": {"uid": "456", "name": "Bob"}},
    ]
    mock_driver, mock_session = mock_neo4j_driver_with_session(
        mock_records=mock_records
    )
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.get("/people")

    # assert
    assert response.status_code == 200
    assert response.json() == [
        {"uid": "123", "name": "Alice"},
        {"uid": "456", "name": "Bob"},
    ]

    mock_session.run.assert_called_once_with("MATCH (p:Person) RETURN p")


def test_create_person(client):
    # arrange
    person_name = "Alice"
    mock_driver, mock_session = mock_neo4j_driver_with_session()
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.post("/people", json={"name": person_name})

    # assert
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == person_name
    assert isinstance(data["uid"], str)
    assert str(uuid.UUID(data["uid"])) == data["uid"]

    mock_session.run.assert_called_once_with(
        "CREATE (p:Person {uid: $uid, name: $name})", uid=ANY, name=person_name
    )


def test_get_person_found(client):
    # arrange
    person = {"uid": "123", "name": "Alice"}
    mock_driver, mock_session = mock_neo4j_driver_with_session(
        single_record={"p": person}
    )
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.get(f"/people/{person['uid']}")

    # assert
    assert response.status_code == 200
    assert response.json() == person

    mock_session.run.assert_called_once_with(
        "MATCH (p:Person {uid: $uid}) RETURN p", uid=person["uid"]
    )


def test_get_person_not_found(client):
    # arrange
    person = {"uid": "123", "name": "does-not-exist"}
    mock_driver, mock_session = mock_neo4j_driver_with_session(single_record=None)
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.get(f"/people/{person['uid']}")

    # assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Person not found"

    mock_session.run.assert_called_once_with(
        "MATCH (p:Person {uid: $uid}) RETURN p", uid=person["uid"]
    )


@pytest.mark.xfail(reason="Currently no UUID validation on person_id path param")
def test_get_person_invalid_uuid(client):
    # act
    response = client.get("/people/not-a-valid-uuid")

    # assert
    # 422 corresponds to Unprocessable Entity in pydantic validation
    assert response.status_code == 422


def test_delete_person_success(client):
    # arrange
    person = {"uid": "123", "name": "does-not-exist"}
    mock_driver, mock_session = mock_neo4j_driver_with_session(
        single_record={"deleted_count": 1}
    )
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.delete(f"/people/{person['uid']}")

    # assert
    assert response.status_code == 200
    assert f"Person {person['uid']} deleted successfully" in response.json()["message"]

    mock_session.run.assert_called_once_with(
        "MATCH (p:Person {uid: $uid}) DELETE p RETURN COUNT(p) AS deleted_count",
        uid=person["uid"],
    )


def test_delete_person_not_found(client):
    # arrange
    person = {"uid": "123", "name": "does-not-exist"}
    mock_driver, mock_session = mock_neo4j_driver_with_session(
        single_record={"deleted_count": 0}
    )
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.delete(f"/people/{person['uid']}")

    # assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Person not found"

    mock_session.run.assert_called_once_with(
        "MATCH (p:Person {uid: $uid}) DELETE p RETURN COUNT(p) AS deleted_count",
        uid=person["uid"],
    )


def test_delete_person_multiple_deleted(client):
    # arrange
    mock_driver, mock_session = mock_neo4j_driver_with_session(
        single_record={"deleted_count": 2}
    )
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.delete("/people/duplicate")

    # assert
    assert response.status_code == 500
    assert "Multiple people deleted" in response.json()["detail"]

    mock_session.run.assert_called_once_with(
        "MATCH (p:Person {uid: $uid}) DELETE p RETURN COUNT(p) AS deleted_count",
        uid="duplicate",
    )


@pytest.mark.xfail(reason="Currently no UUID validation on person_id path param")
def test_delete_person_invalid_uuid(client):
    # act
    response = client.delete("/people/not-a-valid-uuid")

    # assert
    # 422 corresponds to Unprocessable Entity in pydantic validation
    assert response.status_code == 422
