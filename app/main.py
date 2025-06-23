from fastapi import FastAPI
from app.routes import aluno
from app.database.connection import engine, Base
from app import models  # para importar as classes dos modelos e registrá-los

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(aluno.router)
