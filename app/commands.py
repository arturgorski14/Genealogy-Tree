from neo4j import ManagedTransaction, Record


def add_person(tx: ManagedTransaction, name: str) -> None:
    tx.run("CREATE (p:Person {name: $name})", name=name)


def get_person(tx: ManagedTransaction, name: str) -> Record:
    return tx.run("MATCH (p:Person {name: $name}) RETURN p", name=name).single()


def remove_person(tx: ManagedTransaction, name: str) -> None:
    tx.run("MATCH (p:Person {name: $name}) DETACH DELETE p", name=name)
