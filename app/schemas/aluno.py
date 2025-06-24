from pydantic import BaseModel, EmailStr
from datetime import datetime

class AlunoBase(BaseModel):
    nome: str
    email: EmailStr
    plano_id: int


class AlunoCreate(AlunoBase):
    pass

class AlunoResponse(AlunoBase):
    id: int
    
    class Config:
        from_attributes = True

class CheckinBase(BaseModel):
    aluno_id: int

class CheckinCreate(CheckinBase):
    pass

class CheckinResponse(CheckinBase):
    id: int
    data_hora: datetime
    duracao: int | None
    
    class Config:
        orm_mode = True