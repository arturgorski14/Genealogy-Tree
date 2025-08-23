from dotenv import load_dotenv
from neo4j import GraphDatabase
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str

    class ConfigDict:
        env_file = ".env"


load_dotenv()

settings = Settings.model_validate({})


def get_driver():
    return GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )
