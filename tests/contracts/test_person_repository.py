import pytest

from app.infrastructure.repository import PersonRepository
from tests.conftest import mock_neo4j_driver_with_session
from tests.contracts.repository_contract import PersonRepositoryContract


class TestPersonRepositoryWithNeo4j(PersonRepositoryContract):
    @pytest.fixture
    def repository(self):
        mock_records = [
            {"p": {"uid": "1", "name": "Alice"}},
            {"p": {"uid": "2", "name": "Bob"}},
        ]
        mock_driver, _ = mock_neo4j_driver_with_session(mock_records=mock_records)
        return PersonRepository(mock_driver)

    # @pytest.fixture
    # def repository_with_single(self):
    #     single_record = {"p": {"uid": "1", "name": "Alice"}}
    #     mock_driver, _ = mock_neo4j_driver_with_session(single_record=single_record)
    #     return PersonRepository(mock_driver)
