import uuid
from typing import Protocol
from unittest.mock import MagicMock

from neo4j import Neo4jDriver

from app.domain.person import Person


class PersonRepositoryInterface(Protocol):
    def get_all(self) -> list[Person]: ...

    def get(self, uid: str) -> Person | None: ...

    def create(self, name: str) -> Person: ...


class PersonRepository(PersonRepositoryInterface):
    def __init__(self, driver: Neo4jDriver):
        self._driver = driver

    def get_all(self) -> list[Person]:
        with self._driver.session() as session:
            result = session.run("MATCH (p:Person) RETURN p")
            return [Person(uid=r["p"]["uid"], name=r["p"]["name"]) for r in result]

    def get(self, uid: str) -> Person | None:
        with self._driver.session() as session:
            result = session.run("MATCH (p:Person {uid: $uid}) RETURN p", uid=uid)
            record = result.single()
            if record:
                person = record["p"]
                return Person(uid=person["uid"], name=person["name"])
            return None

    def create(self, name: str) -> Person:
        with self._driver.session() as session:
            uid = str(uuid.uuid4())
            result = session.run(
                "CREATE (p:Person {uid: $uid, name: $name}) RETURN p",
                uid=uid,
                name=name,
            )
            record = result.single()
            if not record:
                raise PersonCreationError("Database did not return created person")
            person = record["p"]
            return Person(uid=person["uid"], name=person["name"])


class FakePersonRepository(PersonRepositoryInterface):
    def __new__(cls, *args, **kwargs):
        return MagicMock(spec=PersonRepositoryInterface)


class PersonCreationError(RuntimeError):
    """Raised when a person could not be created in the repository."""
