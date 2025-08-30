from app.application.generics import Query
from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.domain.person import Person
from app.infrastructure.repository import PersonRepositoryInterface


class GetAllPeopleHandler:
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetAllPeopleQuery) -> list[Person]:
        return self._repository.get_all()


class GetPersonHandler:
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetPersonQuery) -> Person | None:
        return self._repository.get(uid=query.uid)


class FakeHandler:
    def __init__(self, repository: PersonRepositoryInterface = None):
        self._repository = repository

    def handle(self, query: Query) -> str:
        return "handled"
