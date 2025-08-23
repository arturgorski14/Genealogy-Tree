from neo4j import Driver, GraphDatabase

from app.config import (
    NEO4J_PASSWORD,
    NEO4J_PASSWORD_FOR_TESTS,
    NEO4J_URI,
    NEO4J_URI_FOR_TESTS,
    NEO4J_USER,
    NEO4J_USER_FOR_TESTS,
)


def get_driver() -> Driver:
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def get_test_driver() -> Driver:
    return GraphDatabase.driver(
        NEO4J_URI_FOR_TESTS,
        auth=(NEO4J_USER_FOR_TESTS, NEO4J_PASSWORD_FOR_TESTS),
    )
