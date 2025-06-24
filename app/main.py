from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import aluno
from app.database.connection import engine, Base
from app import models 

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aluno.router)
