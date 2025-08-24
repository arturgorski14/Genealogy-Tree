from app.domain.person import Person
from app.infrastructure.repository import PersonRepositoryInterface


class FakeRepository(PersonRepositoryInterface):
    def __init__(self, driver=None):
        self._data = [Person(uid="1", name="Alice"), Person(uid="2", name="Bob")]
        self._called_method = None
        self._called_args = None

    def get_all(self):
        self._called_method = "get_all"
        return self._data

    def get(self, uid: str):
        self._called_method = "get"
        self._called_args = uid
        return next((p for p in self._data if p.uid == uid), None)
