from app.application.command_handlers import CreatePersonHandler
from app.application.commands import CreatePersonCommand


def test_create_person_handler_delegates(person_repo):
    # Arrange
    payload = {"name": "fake"}
    handler = CreatePersonHandler(person_repo)
    command = CreatePersonCommand

    # Act
    handler.handle(command(**payload))

    # Assert
    person_repo.create.assert_called_once_with(**payload)


# TODO: test for delete command handler
