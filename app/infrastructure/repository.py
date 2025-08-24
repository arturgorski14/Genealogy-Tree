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
