from starlette import status

from app.application.bus import CommandBus
from app.application.command_handlers import AddParentChildRelationHandler
from app.application.commands import AddParentChildRelationCommand
from app.bootstrap import get_command_bus
from app.infrastructure.repository import PersonRepository
from app.main import app
from tests.conftest import mock_neo4j_driver_with_session


def test_add_parent_child_relationship(client):
    body = {"parent_id": "p1", "child_id": "c1"}
    single_record = {"created": True}
    driver, mock_session = mock_neo4j_driver_with_session(single_record=single_record)
    repo = PersonRepository(driver=driver)
    fake_bus = CommandBus()
    fake_bus.register(
        AddParentChildRelationCommand, AddParentChildRelationHandler(repo)
    )

    app.dependency_overrides[get_command_bus] = lambda: fake_bus

    response = client.post("/people/relationships/parent-child", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data == {"status": "relationship_created"}

    mock_session.run.assert_called_once()


def test_add_parent_child_prevents_cycle():
    driver, mock_session = mock_neo4j_driver_with_session(
        single_record={"created": False}
    )
    repo = PersonRepository(driver=driver)

    created = repo.add_parent_child("a", "b")

    assert created is False
    cypher = mock_session.run.call_args[0][0]
    assert "OPTIONAL MATCH path" in cypher
