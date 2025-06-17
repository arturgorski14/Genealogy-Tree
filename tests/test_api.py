import uuid
from unittest.mock import ANY, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_driver


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


def test_create_person(client):
    # arrange
    mock_session = MagicMock()
    mock_driver = MagicMock()
    mock_driver.session.return_value.__enter__.return_value = mock_session
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.post("/people", json={"name": "Alice"})

    # assert
    mock_session.run.assert_called_once_with(
        "CREATE (p:Person {uid: $uid, name: $name})", uid=ANY, name="Alice"
    )

    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Alice"
    uid = data["uid"]
    assert isinstance(uid, str)
    uuid_obj = uuid.UUID(uid)
    assert str(uuid_obj) == uid
