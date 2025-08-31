from dataclasses import dataclass

from app.application.generics import Query
from app.domain.person import Person


@dataclass
class GetAllPeopleQuery(Query[list[Person]]):
    pass  # no fields needed since we want all users


@dataclass
class GetPersonQuery(Query[Person | None]):
    uid: str
