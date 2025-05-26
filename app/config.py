import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all((NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)):
    raise EnvironmentError(
        "Improperly setup '.env' file. Please check the README.md and adjust."
    )
