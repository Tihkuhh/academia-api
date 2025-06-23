from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.connection import Base
from sqlalchemy.orm import relationship


class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    plano = Column(String)

    checkins = relationship("Checkin", back_populates="aluno", cascade="all, delete")
    
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class Checkin(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"))
    data_hora = Column(DateTime, nullable=False)
    duracao = Column(Integer, nullable=True)

    aluno = relationship("Aluno", back_populates="checkins")
