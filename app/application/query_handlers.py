from app.infrastructure.repository import PersonRepositoryInterface


class GetAllPeopleHandler:
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, query):
        return self._repository.get_all()


class GetPersonHandler:
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, query):
        return self._repository.get(query.uid)


class FakeHandler:
    def __init__(self, repository: PersonRepositoryInterface = None):
        self._repository = repository

    def handle(self, query):
        return "handled"
