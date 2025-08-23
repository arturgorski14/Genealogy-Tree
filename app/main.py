from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import people

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(people.router, prefix="/people", tags=["people"])
