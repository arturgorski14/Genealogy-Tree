import pytest
from starlette import status

from app.application.bus import QueryBus
from app.application.queries import GetPersonQuery
from app.bootstrap import get_query_bus
from app.main import app


def test_get_nonexistent_person(client):
    # Arrange
    class FakeHandler:
        def handle(self, query):
            return None

    fake_bus = QueryBus()
    fake_bus.register(GetPersonQuery, FakeHandler())
    app.dependency_overrides[get_query_bus] = lambda: fake_bus

    # Act
    response = client.get("/people/non-existent-uid")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Person not found"}


@pytest.mark.skip(reason="Not implemented yet")
def test_get_person_with_invalid_uid(): ...


def test_get_person(client):
    # Arrange
    uid = "123"

    class FakeHandler:
        def handle(self, query):
            return {"uid": uid, "name": "Alice"}

    fake_bus = QueryBus()
    fake_bus.register(GetPersonQuery, FakeHandler())

    app.dependency_overrides[get_query_bus] = lambda: fake_bus

    # Act
    response = client.get(f"/people/{uid}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"uid": uid, "name": "Alice"}
