from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

from app.infrastructure.repository import FakePersonRepository
from app.main import app


@pytest.fixture(autouse=True)
def reset_dependency_overrides():
    yield
    app.dependency_overrides = {}


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def mock_neo4j_driver_with_session(mock_records=None, single_record=None):
    """
    Mocks a Neo4j driver with a session, returning
    mock_records for iteration
    single_record for .single()
    """
    mock_session = MagicMock()
    mock_session.run.return_value = MagicMock(
        __iter__=lambda self: iter(mock_records or []),
        single=MagicMock(return_value=single_record),
    )
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    return mock_driver, mock_session


@pytest.fixture
def mocked_driver_with_data():
    _data = [
        {"p": {"uid": "1", "name": "Alice"}},
        {"p": {"uid": "2", "name": "Bob"}},
    ]
    return mock_neo4j_driver_with_session(mock_records=_data)[0]


@pytest.fixture
def mocked_driver_with_single_record():
    _data = {"p": {"uid": "1", "name": "Alice"}}
    return mock_neo4j_driver_with_session(single_record=_data)[0]


@pytest.fixture
def mocked_driver_without_data():
    return mock_neo4j_driver_with_session()[0]


@pytest.fixture
def repo():
    return FakePersonRepository()
