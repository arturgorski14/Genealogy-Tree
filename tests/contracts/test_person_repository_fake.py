import pytest

from app.infrastructure.repository import FakePersonRepository
from tests.contracts.repository_contract import PersonRepositoryContract


class TestPersonRepositoryWithFake(PersonRepositoryContract):
    @pytest.fixture
    def repository(self):
        return FakePersonRepository()
