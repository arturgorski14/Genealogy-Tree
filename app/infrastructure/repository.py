from typing import Protocol

from neo4j import Neo4jDriver

from app.domain.person import Person


class PersonRepositoryInterface(Protocol):
    def get_all(self) -> list[Person]: ...

    def get(self, uid: str) -> Person | None: ...


class PersonRepository(PersonRepositoryInterface):
    def __init__(self, driver: Neo4jDriver):
        self.driver = driver

    def get_all(self) -> list[Person]:
        with self.driver.session() as session:
            result = session.run("MATCH (p:Person) RETURN p")
            return [Person(uid=r["p"]["uid"], name=r["p"]["name"]) for r in result]

    def get(self, uid: str) -> Person | None:
        with self.driver.session() as session:
            result = session.run("MATCH (p:Person {uid: $uid}) RETURN p", uid=uid)
            record = result.single()
            if record:
                person = record["p"]
                return Person(uid=person["uid"], name=person["name"])
            return None


class FakePersonRepository(PersonRepositoryInterface):
    def __init__(self, driver=None, populate: bool = True):
        if populate:
            self._data = [Person(uid="1", name="Alice"), Person(uid="2", name="Bob")]
        else:
            self._data = []
        self._calls = []

    def get_all(self):
        self._calls.append(("get_all", (), {}))
        return self._data

    def get(self, uid: str):
        self._calls.append(("get", (uid,), {}))
        return next((p for p in self._data if p.uid == uid), None)

    def assert_called_once_with(self, method_name: str, *args, **kwargs) -> None:
        matching_calls = [c for c in self._calls if c[0] == method_name]
        if len(matching_calls) != 1:
            raise AssertionError(
                f"Expected {method_name} to be called once. "
                f"Called {len(matching_calls)} times."
            )
        called_args, called_kwargs = matching_calls[0][1], matching_calls[0][2]
        if called_args != args or called_kwargs != kwargs:
            raise AssertionError(
                f"{method_name} called with {called_args}, {called_kwargs}, "
                f"expected {args}, {kwargs}"
            )
