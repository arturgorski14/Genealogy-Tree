from starlette import status

from app.application.bus import QueryBus
from app.application.queries import GetPersonQuery
from app.application.query_handlers import GetPersonHandler
from app.bootstrap import get_query_bus
from app.infrastructure.repository import FakePersonRepository
from app.main import app


def test_get_person(client):
    # Arrange
    uid = "1"
    fake_bus = QueryBus()
    fake_bus.register(GetPersonQuery, GetPersonHandler(FakePersonRepository()))

    app.dependency_overrides[get_query_bus] = lambda: fake_bus
    # Act
    response = client.get(f"/people/{uid}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["uid"] == uid
    assert isinstance(data["name"], str)


def test_get_nonexistent_person(client):
    # Arrange
    fake_bus = QueryBus()
    fake_bus.register(GetPersonQuery, GetPersonHandler(FakePersonRepository()))
    app.dependency_overrides[get_query_bus] = lambda: fake_bus

    # Act
    response = client.get("/people/non-existent-uid")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Person not found"}


def test_get_person_with_invalid_uid(client):
    # Arrange
    fake_bus = QueryBus()
    fake_bus.register(GetPersonQuery, GetPersonHandler(FakePersonRepository()))
    app.dependency_overrides[get_query_bus] = lambda: fake_bus

    # Act
    response = client.get("/people/INVALID_UID")

    # Assert
    # TODO: after parsing, return 422 for invalid UUID, for now treat invalid UID as not found
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Person not found"}
