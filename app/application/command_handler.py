from app.infrastructure.repository import PersonRepositoryInterface


class CreatePersonHandler:
    def __init__(self, repository: PersonRepositoryInterface):
        self._repository = repository

    def handle(self, query):
        return self._repository.create(name=query.name)
