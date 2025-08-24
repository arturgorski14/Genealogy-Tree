class GetAllPeopleHandler:
    def __init__(self, people_repository):
        self.people_repository = people_repository

    def handle(self, query):
        return self.people_repository.get_all()


class GetPersonHandler:
    def __init__(self, repository):
        self.repository = repository

    def handle(self, query):
        return self.repository.get(query.uid)
