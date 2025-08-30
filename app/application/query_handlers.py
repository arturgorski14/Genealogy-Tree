from app.application.generics import Query, QueryHandler
from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.domain.person import Person
from app.infrastructure.repository import PersonRepositoryInterface


class GetAllPeopleHandler(QueryHandler[GetAllPeopleQuery, list[Person]]):
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetAllPeopleQuery) -> list[Person]:
        return self._repository.get_all()


class GetPersonHandler(QueryHandler[GetPersonQuery, Person | None]):
    """A query handler that returns a result of GetPersonQuery"""

    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetPersonQuery) -> Person | None:
        return self._repository.get(uid=query.uid)


class FakeHandler(QueryHandler):
    def __init__(self, repository: PersonRepositoryInterface = None):
        self._repository = repository

    def handle(self, query: Query) -> str:
        return "handled"
