from fastapi import FastAPI
from .routes import students, groups

app = FastAPI()

app.include_router(students.router)
app.include_router(groups.router)