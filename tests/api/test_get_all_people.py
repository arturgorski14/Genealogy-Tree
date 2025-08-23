from fastapi import status

from app.database import get_driver
from app.main import app
from tests.conftest import mock_neo4j_driver_with_session


def test_get_all_people_empty(client):
    # arrange
    mock_driver, mock_session = mock_neo4j_driver_with_session(mock_records=[])
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.get("/people")

    # assert
    assert response.status_code == status.HTTP_200_OK
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
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"uid": "123", "name": "Alice"},
        {"uid": "456", "name": "Bob"},
    ]

    mock_session.run.assert_called_once_with("MATCH (p:Person) RETURN p")
