from neo4j import ManagedTransaction

def add_person(tx: ManagedTransaction, name: str) -> None:
    tx.run("CREATE (p:Person {name: $name})", name=name)
