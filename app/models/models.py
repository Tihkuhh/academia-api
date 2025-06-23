from sqlalchemy import Column, Integer, String
from app.database.connection import Base


class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    plano = Column(String)

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class Checkin(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    data_hora = Column(DateTime(timezone=True), server_default=func.now())

    aluno = relationship("Aluno", backref="checkins")
