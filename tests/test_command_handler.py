from app.application.command_handler import CreatePersonHandler
from app.application.commands import CreatePersonCommand
from app.infrastructure.repository import FakePersonRepository


def test_create_person_handler_delegates():
    # Arrange
    payload = {"name": "fake"}  # TODO: change payload for something more meaningful
    repo = FakePersonRepository()
    handler = CreatePersonHandler(repo)
    command = CreatePersonCommand

    # Act
    handler.handle(command(**payload))

    # Assert
    repo.assert_called_once_with("create", **payload)
