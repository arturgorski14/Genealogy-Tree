from app.application.commands import CreatePersonCommand
from app.domain.person import Person
from app.infrastructure.repository import PersonRepositoryInterface


class CreatePersonHandler:
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, command: CreatePersonCommand) -> Person:
        return self._repository.create(name=command.name)
