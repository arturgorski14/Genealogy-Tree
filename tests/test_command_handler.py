from app.application.command_handlers import CreatePersonHandler, DeletePersonHandler
from app.application.commands import CreatePersonCommand, DeletePersonCommand


def test_create_person_handler_delegates(person_repo):
    # Arrange
    payload = {"name": "fake"}
    handler = CreatePersonHandler(person_repo)
    command = CreatePersonCommand

    # Act
    handler.handle(command(**payload))

    # Assert
    person_repo.create.assert_called_once_with(**payload)


def test_delete_person_handler_delegates(person_repo):
    # Arrange
    payload = {"uid": "fake-uid"}
    handler = DeletePersonHandler(person_repo)
    command = DeletePersonCommand

    # Act
    handler.handle(command(**payload))

    # Assert
    person_repo.delete.assert_called_once_with(**payload)
