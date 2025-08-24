from app.domain.person import Person


class FakeRepo:
    def __init__(self):
        self._data = [Person(uid="1", name="Alice"), Person(uid="2", name="Bob")]

    def get_all(self):
        return self._data

    def get(self, uid: str):
        return next((p for p in self._data if p.uid == uid), None)
