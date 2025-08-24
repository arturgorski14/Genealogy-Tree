import pytest

from tests.contracts.repository_contract import PersonRepositoryContract
from tests.fakes import FakeRepo


class TestPersonRepositoryWithFake(PersonRepositoryContract):
    @pytest.fixture
    def repository(self):
        return FakeRepo()
