import pytest
from starlette import status

from app.application.bus import CommandBus
from app.application.command_handlers import CreatePersonHandler
from app.application.commands import CreatePersonCommand
from app.bootstrap import get_command_bus
from app.infrastructure.repository import PersonRepository
from app.main import app
from tests.conftest import mock_neo4j_driver_with_session


def test_create_person(client):
    # Arrange
    name = "fake-person"
    single_record = {"p": {"uid": "fake-uid", "name": name}}
    driver, _ = mock_neo4j_driver_with_session(single_record=single_record)
    repo = PersonRepository(driver=driver)
    fake_bus = CommandBus()
    fake_bus.register(CreatePersonCommand, CreatePersonHandler(repo))

    app.dependency_overrides[get_command_bus] = lambda: fake_bus

    # Act
    response = client.post("/people/", json={"name": name})
    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert isinstance(data, dict)
    assert set(data.keys()) == {"uid", "name"}  # ensure schema
    assert data["name"] == name
    assert isinstance(data["uid"], str) and data["uid"] != ""


@pytest.mark.skip(reason="Validation not implemented yet")
def test_create_person_with_invalid_characters(): ...
