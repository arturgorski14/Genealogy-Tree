from neo4j import GraphDatabase, Driver
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

driver: Driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
test_driver: Driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_driver() -> Driver:
    return driver

def get_test_driver() -> Driver:
    return driver  # TODO: since the app is still in development stage this work for now
