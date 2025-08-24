from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.application.query_handlers import GetAllPeopleHandler, GetPersonHandler
from app.domain.person import Person


class FakeRepo:
    _data = [Person(uid="1", name="Alice")]

    def get_all(self):
        return self._data

    def get(self, uid: str):
        return next((p for p in self._data if p.uid == uid), None)


def test_get_all_people_handler_uses_repo():
    # Arrange
    handler = GetAllPeopleHandler(FakeRepo())
    query = GetAllPeopleQuery()

    # Act
    result = handler.handle(query)

    # Assert
    assert result == [Person(uid="1", name="Alice")]


def test_get_person():
    # Arrange
    handler = GetPersonHandler(FakeRepo())
    query = GetPersonQuery("1")

    # Act
    result = handler.handle(query)

    # Assert
    assert result == Person(uid="1", name="Alice")


def test_try_to_get_person():
    # Arrange
    handler = GetPersonHandler(FakeRepo())
    query = GetPersonQuery("non-existent")

    # Act
    result = handler.handle(query)

    # Assert
    assert result is None
