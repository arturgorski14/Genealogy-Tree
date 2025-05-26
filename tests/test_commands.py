import pytest
from neo4j import Driver, Record, Result

from app.commands import add_person
from app.db import get_test_driver

driver: Driver = get_test_driver()


@pytest.fixture(scope="module")
def neo4j_session():
    with driver.session() as session:
        yield session
    driver.close()


def test_add_person_creates_node(neo4j_session):
    person_name: str = "TestUser123"

    # Cleanup
    neo4j_session.run(
        "MATCH (p:Person {name: $name}) DETACH DELETE p", name=person_name
    )

    neo4j_session.execute_write(add_person, person_name)

    result: Result = neo4j_session.run(
        "MATCH (p:Person {name: $name}) RETURN p", name=person_name
    )
    person_node: Record = result.single()

    assert person_node is not None
    assert person_node["p"]["name"] == person_name
