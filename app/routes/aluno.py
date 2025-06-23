from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.aluno import AlunoCreate, AlunoResponse
from app.database.connection import SessionLocal, get_db
from app.schemas.aluno import CheckinCreate, CheckinResponse
import joblib
import os
import pika
import json
from app.models.models import Aluno, Checkin
from datetime import datetime, timezone


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/aluno/registro", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    existing = db.query(Aluno).filter(Aluno.email == aluno.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo_aluno = Aluno(nome=aluno.nome, email=aluno.email, plano=aluno.plano)
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno

@router.post("/aluno/checkin")
def registrar_checkin(checkin: CheckinCreate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == checkin.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    publicar_checkin_fila(checkin.aluno_id)

    return {"mensagem": "Check-in enviado para processamento."}


@router.get("/aluno/{id}/frequencia", response_model=list[CheckinResponse])
def listar_checkins(id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    return aluno.checkins



# Carrega o modelo só uma vez, quando o módulo é importado
model_path = os.path.join(os.path.dirname(__file__), "../../ml/churn_model.pkl")
modelo_churn = joblib.load(model_path)

@router.get("/aluno/{id}/risco-churn")



def obter_risco_churn(id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Calcular as features para o modelo (simplificado)

    # Frequência semanal: número de checkins na última semana
    from datetime import datetime, timedelta, timezone
    agora = datetime.now(timezone.utc)
    semana_atras = agora - timedelta(days=7)

    checkins_ultima_semana = (
        db.query(Checkin)
        .filter(Checkin.aluno_id == id, Checkin.data_hora >= semana_atras)
        .count()
    )

    # Dias desde o último checkin
    ultimo_checkin = (
        db.query(Checkin)
        .filter(Checkin.aluno_id == id)
        .order_by(Checkin.data_hora.desc())
        .first()
    )
    if ultimo_checkin:
        dias_desde_ultimo = (agora - ultimo_checkin.data_hora).days
    else:
        dias_desde_ultimo = 999  # Muito tempo sem checkin

    # Duração média das visitas - para simplificar, vamos fixar como 45 min (você pode melhorar depois)
    duracao_media = 45

    # Tipo do plano: suponha que mensal = 0, anual = 1
    tipo_plano = 0 if aluno.plano == "mensal" else 1

    # Montar vetor de features para previsão
    features = [[checkins_ultima_semana, dias_desde_ultimo, duracao_media, tipo_plano]]

    # Prever churn
    probabilidade_churn = modelo_churn.predict_proba(features)[0][1]  # Probabilidade de churn = 1

    return {
        "aluno_id": aluno.id,
        "nome": aluno.nome,
        "probabilidade_churn": probabilidade_churn
    }
def publicar_checkin_fila(aluno_id: int):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='checkins', durable=True)

    mensagem = json.dumps({'aluno_id': aluno_id})
    channel.basic_publish(
        exchange='',
        routing_key='checkins',
        body=mensagem,
        properties=pika.BasicProperties(
            delivery_mode=2,  # mensagem persistente
        )
    )
    connection.close()
