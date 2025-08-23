class PeopleRepository:
    def __init__(self, driver):
        self.driver = driver

    def get_all(self):
        with self.driver.session() as session:
            result = session.run("MATCH (p:Person) RETURN p")
            return [{"uid": r["p"]["uid"], "name": r["p"]["name"]} for r in result]


class PersonRepository:
    def __init__(self, driver):
        self.driver = driver

    def get(self, uid: str):
        with self.driver.session() as session:
            result = session.run("MATCH (p:Person {uid: $uid}) RETURN p")
            return result.single()  # TODO: Check the real result in main_cqrs.py
