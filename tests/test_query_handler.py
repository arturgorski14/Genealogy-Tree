from app.application.queries import GetAllPeopleQuery
from app.application.query_handlers import GetAllPeopleHandler


class FakeRepo:
    def get_all(self):
        return [{"uid": "1", "name": "Alice"}]


def test_get_all_people_handler_uses_repo():
    handler = GetAllPeopleHandler(FakeRepo())
    query = GetAllPeopleQuery()

    result = handler.handle(query)

    assert result == [{"uid": "1", "name": "Alice"}]
