from typing import Optional

from app.application.commands import (
    AddParentChildRelationCommand,
    CreatePersonCommand,
    DeletePersonCommand,
)
from app.application.generics import Command, CommandHandler
from app.domain.person import Person
from app.infrastructure.repository import PersonRepositoryInterface


class CreatePersonHandler(CommandHandler):
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, command: CreatePersonCommand) -> Person:
        return self._repository.create(name=command.name)


class AddParentChildRelationHandler:
    def __init__(self, repo: PersonRepositoryInterface):
        self.repo = repo

    def handle(self, cmd: AddParentChildRelationCommand) -> bool:
        return self.repo.add_parent_child(cmd.parent_id, cmd.child_id)


class DeletePersonHandler(CommandHandler):
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, command: DeletePersonCommand) -> bool:
        return self._repository.delete(uid=command.uid)


class FakeCommandHandler(CommandHandler):
    def __init__(self, repository: Optional[PersonRepositoryInterface] = None):
        self._repository = repository

    def handle(self, command: Command) -> str:
        return "handled"
