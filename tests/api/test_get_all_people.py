from fastapi import status

from app.application.bus import QueryBus
from app.application.queries import GetAllPeopleQuery
from app.application.query_handlers import FakeHandler, GetAllPeopleHandler
from app.bootstrap import get_query_bus
from app.infrastructure.repository import FakePersonRepository
from app.main import app


def test_get_all_people_empty(client):
    # Arrange
    fake_bus = QueryBus()
    fake_bus.register(
        GetAllPeopleQuery, GetAllPeopleHandler(FakePersonRepository(populate=False))
    )

    app.dependency_overrides[get_query_bus] = lambda: fake_bus

    # Act
    response = client.get("/people")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_all_people(client):
    # Arrange
    fake_bus = QueryBus()
    fake_bus.register(GetAllPeopleQuery, GetAllPeopleHandler(FakePersonRepository()))

    app.dependency_overrides[get_query_bus] = lambda: fake_bus

    # Act
    response = client.get("/people")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"uid": "1", "name": "Alice"},
        {"uid": "2", "name": "Bob"},
    ]
