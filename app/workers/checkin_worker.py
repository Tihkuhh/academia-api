import pika
import json
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.models import Checkin
from datetime import datetime, timezone

def salvar_checkin(aluno_id: int):
    db: Session = SessionLocal()
    try:
        novo_checkin = Checkin(aluno_id=aluno_id, data_hora=datetime.now(timezone.utc))
        db.add(novo_checkin)
        db.commit()
    except Exception as e:
        print(f"Erro ao salvar checkin: {e}")
    finally:
        db.close()

def callback(ch, method, properties, body):
    dados = json.loads(body)
    aluno_id = dados.get("aluno_id")
    print(f"Processando checkin do aluno {aluno_id}")
    salvar_checkin(aluno_id)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='checkins', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='checkins', on_message_callback=callback)

    print("⏳ Aguardando mensagens de checkin. Pressione CTRL+C para sair.")
    channel.start_consuming()

if __name__ == "__main__":
    main()
