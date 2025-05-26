import logging

from app.commands import add_person
from app.db import get_driver

logging.basicConfig(level=logging.DEBUG)


def main():
    driver = get_driver()

    with driver.session() as session:
        session.run("MATCH (p:Person) DETACH DELETE p")
        session.execute_write(add_person, "Artur")

    driver.close()


if __name__ == "__main__":
    logging.debug("Main start")
    main()
    logging.debug("Main finished")
