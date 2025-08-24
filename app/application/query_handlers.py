from app.infrastructure.repository import PersonRepositoryInterface


class GetAllPeopleHandler:
    def __init__(self, repository: PersonRepositoryInterface):
        self.repository = repository

    def handle(self, query):
        return self.repository.get_all()


class GetPersonHandler:
    def __init__(self, repository: PersonRepositoryInterface):
        self.repository = repository

    def handle(self, query):
        return self.repository.get(query.uid)


class FakeHandler:
    def __init__(self, repository: PersonRepositoryInterface = None):
        self.repository = repository

    def handle(self, query):
        return "handled"
