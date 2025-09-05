from dataclasses import dataclass

from app.application.generics import Command
from app.domain.person import Person


@dataclass
class CreatePersonCommand(Command[Person]):
    name: str


@dataclass
class DeletePersonCommand(Command):
    uid: str
