from fastapi import status

from app.application.bus import QueryBus
from app.application.queries import GetAllPeopleQuery
from app.bootstrap import get_query_bus
from app.main import app


def test_get_all_people_empty(client):
    # Arrange
    class FakeHandler:
        def handle(self, query):
            return []

    fake_bus = QueryBus()
    fake_bus.register(GetAllPeopleQuery, FakeHandler())

    app.dependency_overrides[get_query_bus] = lambda: fake_bus

    # Act
    response = client.get("/people")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_all_people(client):
    # Arrange
    class FakeHandler:
        def handle(self, query):
            return [
                {"uid": "123", "name": "Alice"},
                {"uid": "456", "name": "Bob"},
            ]

    fake_bus = QueryBus()
    fake_bus.register(GetAllPeopleQuery, FakeHandler())

    app.dependency_overrides[get_query_bus] = lambda: fake_bus

    # Act
    response = client.get("/people")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"uid": "123", "name": "Alice"},
        {"uid": "456", "name": "Bob"},
    ]
