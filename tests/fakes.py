from app.domain.person import Person
from app.infrastructure.repository import PersonRepositoryInterface


class FakeRepository(PersonRepositoryInterface):
    def __init__(self, driver=None):
        self._data = [Person(uid="1", name="Alice"), Person(uid="2", name="Bob")]
        self.calls = []

    def get_all(self):
        self.calls.append(("get_all", (), {}))
        return self._data

    def get(self, uid: str):
        self.calls.append(("get", (uid,), {}))
        return next((p for p in self._data if p.uid == uid), None)

    def assert_called_once_with(self, method_name: str, *args, **kwargs) -> None:
        matching_calls = [c for c in self.calls if c[0] == method_name]
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


class FakeHandler:
    def handle(self, query):
        return "handled"
