from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.application.query_handlers import GetAllPeopleHandler, GetPersonHandler
from app.domain.person import Person
from tests.fakes import FakeRepo


def test_get_all_people_handler_uses_repo():
    # Arrange
    handler = GetAllPeopleHandler(FakeRepo())
    query = GetAllPeopleQuery()

    # Act
    result = handler.handle(query)

    # Assert
    assert len(result) == 2
    assert result[0] == Person(uid="1", name="Alice")
    assert result[1] == Person(uid="2", name="Bob")


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
