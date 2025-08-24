import pytest

from tests.contracts.repository_contract import PersonRepositoryContract
from tests.fakes import FakeRepository


class TestPersonRepositoryWithFake(PersonRepositoryContract):
    @pytest.fixture
    def repository(self):
        return FakeRepository()
