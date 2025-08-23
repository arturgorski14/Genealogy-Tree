class GetAllPeopleHandler:
    def __init__(self, people_repository):
        self.people_repository = people_repository

    def handle(self, query):
        return self.people_repository.get_all()
