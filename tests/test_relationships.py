import uuid
from unittest.mock import MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.database import get_driver
from app.main import app
from app.models import ParentRelationshipInput, ParentType, Person


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_dependency_overrides():
    yield
    app.dependency_overrides = {}


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


def test_get_all_relationships_empty(client):
    # arrange
    mock_records = []
    mock_driver, mock_session = mock_neo4j_driver_with_session(
        mock_records=mock_records
    )
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.get("/relationships/")

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_records

    expected_query = (
        "MATCH (parent:Person)-[r:PARENT]->(child:Person)"
        " RETURN parent.uid AS parent_id, child.uid AS child_id, r.type AS type"
    )
    mock_session.run.assert_called_once_with(expected_query)


def test_get_all_relationships(client):
    # arrange
    mock_records = [
        {"parent_id": "1", "child_id": "2", "type": "father"},
        {"parent_id": "3", "child_id": "4", "type": "mother"},
    ]
    mock_driver, mock_session = mock_neo4j_driver_with_session(
        mock_records=mock_records
    )
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.get("/relationships/")

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_records

    expected_query = (
        "MATCH (parent:Person)-[r:PARENT]->(child:Person)"
        " RETURN parent.uid AS parent_id, child.uid AS child_id, r.type AS type"
    )
    mock_session.run.assert_called_once_with(expected_query)


def test_create_relationship(client):
    # arrange
    child = Person(uid=uuid.uuid4(), name="Child")
    parent = Person(uid=uuid.uuid4(), name="Father")
    mock_driver, mock_session = mock_neo4j_driver_with_session()
    app.dependency_overrides[get_driver] = lambda: mock_driver

    rel = ParentRelationshipInput(
        parent_id=parent.uid, child_id=child.uid, type=ParentType.father
    )
    # act
    response = client.post(
        "/relationships/parent",
        json={
            "parent_id": str(rel.parent_id),
            "child_id": str(rel.child_id),
            "type": rel.type.value,
        },
    )

    # assert
    assert response.status_code == status.HTTP_200_OK

    expected_query = (
        "MATCH (child:Person {uid: $child_id}), (parent:Person {uid: $parent_id})"
        " MERGE (parent)-[r:PARENT]->(child)"
        " SET r.type = $type"
    )

    mock_session.run.assert_called_once_with(
        expected_query,
        parent_id=str(rel.parent_id),
        child_id=str(rel.child_id),
        type=rel.type.value,
    )


def test_delete_parent_relationship(client):
    # arrange
    child = Person(uid=uuid.uuid4(), name="Child")
    parent = Person(uid=uuid.uuid4(), name="Father")
    mock_driver, mock_session = mock_neo4j_driver_with_session(
        single_record={"deleted_count": 1}
    )
    app.dependency_overrides[get_driver] = lambda: mock_driver

    rel = ParentRelationshipInput(
        parent_id=parent.uid, child_id=child.uid, type=ParentType.father
    )
    # act
    response = client.delete(f"/relationships/{str(rel.parent_id)}/{str(rel.child_id)}")

    # assert
    assert response.status_code == status.HTTP_200_OK

    expected_query = (
        "MATCH (parent:Person {uid: $parent_id})-[r:PARENT]->"
        "(child:Person {uid: $child_id})"
        " DELETE r RETURN count(r) AS deleted_count"
    )

    mock_session.run.assert_called_once_with(
        expected_query, parent_id=str(rel.parent_id), child_id=str(rel.child_id)
    )


def test_delete_parent_relationship_not_found(client):
    # arrange
    parent_id = str(uuid.uuid4())
    child_id = str(uuid.uuid4())
    mock_driver, mock_session = mock_neo4j_driver_with_session(
        single_record={"deleted_count": 0}
    )
    app.dependency_overrides[get_driver] = lambda: mock_driver

    # act
    response = client.delete(f"/relationships/{parent_id}/{child_id}")

    # assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

    expected_query = (
        "MATCH (parent:Person {uid: $parent_id})-[r:PARENT]->"
        "(child:Person {uid: $child_id})"
        " DELETE r RETURN count(r) AS deleted_count"
    )

    mock_session.run.assert_called_once_with(
        expected_query, parent_id=parent_id, child_id=child_id
    )
