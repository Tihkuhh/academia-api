# app/models/models.py (atualizado)
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.connection import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Plano(Base):
    __tablename__ = "planos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False)    
    alunos = relationship("Aluno", back_populates="plano")

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    # Campos existentes:
    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=False)
    plano = relationship("Plano", back_populates="alunos")
    checkins = relationship("Checkin", back_populates="aluno", cascade="all, delete")

class Checkin(Base):
    __tablename__ = "checkins"
    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"))
    data_hora = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    duracao = Column(Integer, nullable=True)
    aluno = relationship("Aluno", back_populates="checkins")