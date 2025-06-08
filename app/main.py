# import uuid

from fastapi import FastAPI  # , HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_driver

# from app.models import Person

app = FastAPI()
driver = get_driver()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/people")
def get_all_people():
    print("Getting people")
    with driver.session() as session:
        result = session.run("MATCH (p:Person) RETURN p")
        return [record["p"] for record in result]


# @app.get("/people/{person_id}")
# def get_person(person_id: str):
#     print("Getting person")
#     with driver.session() as session:
#         result = session.run("MATCH (p:Person {id: $id}) RETURN p", id=person_id)  # noqa E501
#         record = result.single()
#         if record:
#             return record["p"]
#         raise HTTPException(status_code=404, detail="Person not found")
#
# @app.post("/people")
# def create_person(person: Person):
#     print("Creating person")
#     person.id = str(uuid.uuid4())
#     with driver.session() as session:
#         session.run(
#             "CREATE (p:Person {id: $id, name: $name)",
#             id=person.id,
#             name=person.name
#         )
#     return person
