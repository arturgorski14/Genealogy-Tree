from fastapi import status

from app.application.bus import QueryBus
from app.application.queries import GetAllPeopleQuery
from app.application.query_handlers import GetAllPeopleHandler
from app.bootstrap import get_query_bus
from app.infrastructure.repository import PersonRepository
from app.main import app


def test_get_all_people_empty(client, mocked_driver_without_data):
    # Arrange
    repo = PersonRepository(driver=mocked_driver_without_data)
    fake_bus = QueryBus()
    fake_bus.register(GetAllPeopleQuery, GetAllPeopleHandler(repo))

    app.dependency_overrides[get_query_bus] = lambda: fake_bus

    # Act
    response = client.get("/people")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_all_people(client, mocked_driver_with_data):
    # Arrange
    repo = PersonRepository(driver=mocked_driver_with_data)
    fake_bus = QueryBus()
    fake_bus.register(GetAllPeopleQuery, GetAllPeopleHandler(repo))

    app.dependency_overrides[get_query_bus] = lambda: fake_bus

    # Act
    response = client.get("/people")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"uid": "1", "name": "Alice"},
        {"uid": "2", "name": "Bob"},
    ]
