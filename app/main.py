from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import aluno
from app.database.connection import engine, Base
from app import models  # importa os modelos para registrar

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração de CORS para permitir requisições externas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique a origem do frontend aqui
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aluno.router)
