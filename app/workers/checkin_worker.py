import pika
import json
import time
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.models import Checkin
from datetime import datetime, timezone

def salvar_checkin(aluno_id: int):
    db: Session = SessionLocal()
    try:
        novo_checkin = Checkin(
            aluno_id=aluno_id, 
            data_hora=datetime.now(timezone.utc)
        )
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

# tenta conectar várias vezes ao RabbitMQ
def wait_for_rabbitmq():
    MAX_RETRIES = 5
    RETRY_DELAY = 5  # segundos

    for i in range(MAX_RETRIES):
        try:
            print(f"🐇 Tentando conectar ao RabbitMQ... tentativa {i+1}")
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            print("✅ Conectado ao RabbitMQ.")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"❌ Conexão falhou, tentando novamente em {RETRY_DELAY} segundos...")
            time.sleep(RETRY_DELAY)
    raise Exception("❌ Não foi possível conectar ao RabbitMQ após várias tentativas.")

def main():
    connection = wait_for_rabbitmq()  # função com retry
    channel = connection.channel()
    channel.queue_declare(queue='checkins', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='checkins', on_message_callback=callback)

    print("⏳ Aguardando mensagens de checkin. Pressione CTRL+C para sair.")
    channel.start_consuming()

if __name__ == "__main__":
    main()
