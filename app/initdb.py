from app.database.connection import engine, SessionLocal, Base
from app.models.models import Aluno, Plano, Checkin
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')  # Português do Brasil

def init_db():
    print("🔧 Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

    db = SessionLocal()
    try:
        # Criar planos padrão
        print("📦 Inserindo planos padrão...")
        planos_data = planos_data = [
    {"nome": "mensal"},
    {"nome": "anual"}
]
        
        planos_objs = []
        for plano_data in planos_data:
            # SEMPRE obtém ou cria o plano
            plano = db.query(Plano).filter_by(nome=plano_data["nome"]).first()
            if not plano:
                plano = Plano(**plano_data)
                db.add(plano)
                db.commit()  # Commit imediato para gerar ID
                print(f"✅ Plano {plano_data['nome']} criado")
            else:
                print(f"ℹ️ Plano {plano_data['nome']} já existe")
            planos_objs.append(plano)  # ADICIONA MESMO SE JÁ EXISTIR
        
        print(f"📊 Total de planos disponíveis: {len(planos_objs)}")
        
        # Criar 50 alunos de teste
        print("👥 Criando 50 alunos de teste...")
        alunos_objs = []
        for i in range(50):
            aluno = Aluno(
                nome=fake.name(),
                email=fake.email(),
                plano_id=random.choice([p.id for p in planos_objs])
            )
            db.add(aluno)
            alunos_objs.append(aluno)
            
            # Commit periódico para evitar muita memória
            if i % 10 == 0:
                db.commit()

        db.commit()
        print(f"✅ {len(alunos_objs)} alunos criados com sucesso.")

        # Log adicional para verificação
        print("📊 Resumo de dados:")
        print(f"  - Planos: {db.query(Plano).count()}")
        print(f"  - Alunos: {db.query(Aluno).count()}")
        print(f"  - Checkins: {db.query(Checkin).count()}")
        
        # Criar checkins aleatórios
        print("🏋️ Criando checkins aleatórios...")
        total_checkins = 0
        for aluno in alunos_objs:
            # Cada aluno terá entre 0-20 checkins
            for _ in range(random.randint(0, 20)):
                dias_atras = random.randint(0, 60)  # Checkins nos últimos 60 dias
                horas_atras = random.randint(0, 23)
                minutos_atras = random.randint(0, 59)
                
                checkin = Checkin(
                    aluno_id=aluno.id,
                    data_hora=datetime.utcnow() - timedelta(days=dias_atras, hours=horas_atras, minutes=minutos_atras),
                    duracao=random.randint(30, 120)  # 30-120 minutos
                )
                db.add(checkin)
                total_checkins += 1
        
        db.commit()
        print(f"✅ {total_checkins} checkins criados.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro durante a inicialização: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()