from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.application.query_handlers import GetAllPeopleHandler, GetPersonHandler


class FakeRepo:
    _data = [{"uid": "1", "name": "Alice"}]

    def get_all(self):
        return self._data

    def get(self, uid: str):
        return self._data[0]


def test_get_all_people_handler_uses_repo():
    handler = GetAllPeopleHandler(FakeRepo())
    query = GetAllPeopleQuery()

    result = handler.handle(query)

    assert result == [{"uid": "1", "name": "Alice"}]


def test_get_person():
    handler = GetPersonHandler(FakeRepo())
    query = GetPersonQuery("1")

    result = handler.handle(query)

    assert result == {"uid": "1", "name": "Alice"}


def test_try_to_get_person():
    handler = GetPersonHandler(FakeRepo())
    query = GetPersonQuery("non-existent")

    result = handler.handle(query)

    assert result == {}
