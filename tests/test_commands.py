import pytest
from neo4j import Driver, Record, Session

from app.commands import add_person, get_person, remove_person
from app.database import get_test_driver

PERSON_NAME = "TestAddUser"


@pytest.fixture(scope="module")
def neo4j_driver() -> Driver:
    driver = get_test_driver()
    yield driver
    driver.close()


@pytest.fixture(scope="module")
def neo4j_session(neo4j_driver: Driver) -> Session:
    with neo4j_driver.session() as session:
        yield session


def test_db_connection(neo4j_session: Session):
    """Smoke test to verify database is reachable."""
    result = neo4j_session.run("RETURN 1 AS test")
    assert result.single()["test"] == 1


@pytest.mark.depends(on=["test_db_connection"])
def test_get_person_not_found(neo4j_session):
    neo4j_session.execute_write(remove_person, PERSON_NAME)
    person_node = neo4j_session.execute_read(get_person, PERSON_NAME)
    assert person_node is None, "Expected no person node, but found one."


@pytest.mark.depends(on=["test_db_connection"])
def test_add_person(neo4j_session):
    neo4j_session.execute_write(remove_person, PERSON_NAME)
    neo4j_session.execute_write(add_person, PERSON_NAME)

    person_node = neo4j_session.execute_read(get_person, PERSON_NAME)
    assert person_node is not None, "Person node was not created."
    assert person_node["p"]["name"] == PERSON_NAME


@pytest.mark.depends(on=["test_add_person"])
def test_get_person(neo4j_session):
    person_node: Record = neo4j_session.execute_read(get_person, PERSON_NAME)

    assert person_node is not None, "Expected person node not found."
    assert person_node["p"]["name"] == PERSON_NAME


@pytest.mark.depends(on=["test_get_person"])
def test_remove_person(neo4j_session):
    neo4j_session.execute_write(remove_person, PERSON_NAME)

    person_node = neo4j_session.execute_read(get_person, PERSON_NAME)
    assert person_node is None, "Person node was not deleted."
