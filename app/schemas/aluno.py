from pydantic import BaseModel, EmailStr

class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
    plano: str

class AlunoResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    plano: str

    class Config:
        orm_mode = True

from datetime import datetime

class CheckinCreate(BaseModel):
    aluno_id: int

class CheckinResponse(BaseModel):
    id: int
    aluno_id: int
    data_hora: datetime

    class Config:
        orm_mode = True
