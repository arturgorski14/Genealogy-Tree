from app.application.command_handler import CreatePersonHandler
from app.application.commands import CreatePersonCommand


def test_create_person_handler_delegates(repo):
    # Arrange
    payload = {"name": "fake"}  # TODO: change payload for something more meaningful
    handler = CreatePersonHandler(repo)
    command = CreatePersonCommand

    # Act
    handler.handle(command(**payload))

    # Assert
    repo.create.assert_called_once_with(**payload)
