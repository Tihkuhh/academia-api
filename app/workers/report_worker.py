import os
import csv
import time
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.models import Checkin

def generate_daily_report():
    # Data de ontem (UTC)
    hoje = datetime.now(timezone.utc).date()
    ontem = hoje - timedelta(days=1)
    
    db: Session = SessionLocal()
    try:
        # Busca todos os checkins de ontem
        inicio_ontem = datetime.combine(ontem, datetime.min.time()).replace(tzinfo=timezone.utc)
        fim_ontem = inicio_ontem + timedelta(days=1)

        checkins = db.query(Checkin).filter(
            Checkin.data_hora >= inicio_ontem,
            Checkin.data_hora < fim_ontem
        ).all()
        
        # Cria diretório se não existir
        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)
        
        # Nome do arquivo com data
        filename = os.path.join(report_dir, f"report_{ontem.strftime('%Y-%m-%d')}.csv")
        
        # Escreve o CSV
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'aluno_id', 'data_hora', 'duracao'])
            for checkin in checkins:
                writer.writerow([
                    checkin.id,
                    checkin.aluno_id,
                    checkin.data_hora.isoformat(),
                    checkin.duracao
                ])
        
        print(f"Relatório diário gerado: {filename} com {len(checkins)} registros.")
        return filename
    finally:
        db.close()

def main():
    print("⏰ Worker de relatórios iniciado. Aguardando meia-noite UTC...")
    while True:
        agora = datetime.now(timezone.utc)
        proxima_meia_noite = (agora + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        segundos_para_meia_noite = (proxima_meia_noite - agora).total_seconds()
        time.sleep(segundos_para_meia_noite)
        generate_daily_report()

if __name__ == "__main__":
    main()