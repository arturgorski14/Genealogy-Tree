import pytest

from app.application.queries import GetAllPeopleQuery, GetPersonQuery
from app.application.query_handlers import GetAllPeopleHandler, GetPersonHandler


def test_get_all_people_handler_delegates(person_repo):
    # Arrange
    handler = GetAllPeopleHandler(person_repo)
    query = GetAllPeopleQuery()

    # Act
    handler.handle(query)

    # Assert
    person_repo.get_all.assert_called_once_with()


@pytest.mark.parametrize("uid", ["1", "non-existent"])
def test_get_person_handler_delegates(uid, person_repo):
    # Arrange
    handler = GetPersonHandler(person_repo)
    query = GetPersonQuery(uid)

    # Act
    handler.handle(query)

    # Assert
    person_repo.get.assert_called_once_with(uid=uid)
