from typing import Optional

from app.application.generics import Query, QueryHandler
from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.domain.person import Person
from app.infrastructure.repository import PersonRepositoryInterface


class GetAllPeopleHandler(QueryHandler):
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetAllPeopleQuery) -> list[Person]:
        return self._repository.get_all()


class GetPersonHandler(QueryHandler):
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetPersonQuery) -> Person | None:
        return self._repository.get(uid=query.uid)


class FakeQueryHandler(QueryHandler):
    def __init__(self, repository: Optional[PersonRepositoryInterface] = None):
        self._repository = repository

    def handle(self, query: Query) -> str:
        return "handled"
