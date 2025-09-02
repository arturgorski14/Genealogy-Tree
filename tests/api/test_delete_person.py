from starlette import status

from app.application.bus import CommandBus
from app.application.command_handlers import DeletePersonHandler
from app.application.commands import DeletePersonCommand
from app.bootstrap import get_command_bus
from app.infrastructure.repository import PersonRepository
from app.main import app
from tests.conftest import mock_neo4j_driver_with_session


def test_delete_existing_person(client):
    # Arrange
    single_record = {"deleted_count": 1}
    driver, _ = mock_neo4j_driver_with_session(single_record=single_record)
    repo = PersonRepository(driver=driver)
    fake_bus = CommandBus()
    fake_bus.register(DeletePersonCommand, DeletePersonHandler(repo))

    app.dependency_overrides[get_command_bus] = lambda: fake_bus

    # Act
    response = client.delete("/people/fake-uid")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""  # empty body
