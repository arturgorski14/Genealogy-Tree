from typing import Protocol

from neo4j import Neo4jDriver

from app.domain.person import Person


class PersonRepositoryInterface(Protocol):
    def get_all(self) -> list[Person]: ...

    def get(self, uid: str) -> Person | None: ...


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


class FakePersonRepository(PersonRepositoryInterface):
    def __init__(self, driver: Neo4jDriver = None):
        self._calls = []

    def get_all(self):
        self._calls.append(("get_all", (), {}))
        return []

    def get(self, uid: str):
        self._calls.append(("get", (uid,), {}))
        return None

    def assert_called_once_with(self, method_name: str, *args, **kwargs) -> None:
        matching_calls = [c for c in self._calls if c[0] == method_name]
        assert len(matching_calls) == 1, (
            f"Expected {method_name} to be called once."
            f"Called {len(matching_calls)} times."
        )
        called_args, called_kwargs = matching_calls[0][1], matching_calls[0][2]
        assert called_args == args and called_kwargs == kwargs, (
            f"{method_name} called with {called_args}, {called_kwargs},"
            f"expected {args}, {kwargs}"
        )
