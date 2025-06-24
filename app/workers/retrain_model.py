# app/workers/retrain_model.py
# (Seu código, com a correção abaixo)

import os
import joblib
import pandas as pd
import time
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from app.database.connection import SessionLocal
from app.models.models import Aluno, Checkin

def extract_features(aluno, db):
    # Frequência semanal: número de checkins na última semana
    uma_semana_atras = datetime.now(timezone.utc) - timedelta(days=7)
    
    checkins_ultima_semana = db.query(Checkin).filter(
        Checkin.aluno_id == aluno.id,
        Checkin.data_hora >= uma_semana_atras
    ).count()
    
    # Dias desde o último checkin
    ultimo_checkin = db.query(Checkin).filter(
        Checkin.aluno_id == aluno.id
    ).order_by(Checkin.data_hora.desc()).first()
    
    if ultimo_checkin:
        if ultimo_checkin.data_hora.tzinfo is None:
            ultimo_checkin_utc = ultimo_checkin.data_hora.replace(tzinfo=timezone.utc)
        else:
            ultimo_checkin_utc = ultimo_checkin.data_hora
            
        dias_desde_ultimo = (datetime.now(timezone.utc) - ultimo_checkin_utc).days
    else:
        dias_desde_ultimo = 999
        
    duracao_media = db.query(func.avg(Checkin.duracao)).filter(
        Checkin.aluno_id == aluno.id
    ).scalar() or 0
    
    tipo_plano = 0 if aluno.plano.nome == "mensal" else 1
    
    churn = 1 if dias_desde_ultimo > 30 else 0
    
    # print(f"Aluno ID {aluno.id}: ...") # Log opcional
    
    return {
        'aluno_id': aluno.id,
        'checkins_ultima_semana': checkins_ultima_semana,
        'dias_desde_ultimo': dias_desde_ultimo,
        'duracao_media': duracao_media,
        'tipo_plano': tipo_plano,
        'churn': churn
    }

def train_model():
    print("🔄 Iniciando treinamento do modelo...")
    db = SessionLocal()
    try:
        alunos = db.query(Aluno).options(joinedload(Aluno.plano)).all()
        print(f"🔍 Encontrados {len(alunos)} alunos no banco de dados.")
        
        if len(alunos) < 5:
            print("⚠️ Menos de 5 alunos no banco. Pulando treinamento.")
            return
            
        data = [extract_features(aluno, db) for aluno in alunos]
        df = pd.DataFrame(data)
        
        if df.empty:
            print("⚠️ Nenhum dado disponível para treinamento.")
            return
        
        # --- CORREÇÃO AQUI ---
        # A verificação deve ser no DataFrame, antes de criar X e y
        if len(df) < 5:
            print(f"⚠️ Apenas {len(df)} registros. Dados insuficientes para divisão treino/teste.")
            return

        unique_classes = df['churn'].unique()
        if len(unique_classes) < 2:
            print(f"⚠️ Apenas uma classe presente nos dados: {unique_classes}. Não é possível treinar.")
            return
        # --- FIM DA CORREÇÃO ---
        
        X = df[['checkins_ultima_semana', 'dias_desde_ultimo', 'duracao_media', 'tipo_plano']]
        y = df['churn']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        print("📈 Relatório de Classificação:")
        # Adicionado zero_division=0 para evitar warnings caso uma classe não tenha predições
        print(classification_report(y_test, y_pred, zero_division=0)) 
        
        model_dir = "ml"
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, "churn_model.pkl")
        joblib.dump(model, model_path)
        print(f"✅ Modelo salvo em {model_path}")
        
    except Exception as e:
        print(f"❌ Erro durante o treinamento: {e}")
    finally:
        db.close()

def main():
    print("🔁 Worker de retreinamento de modelo iniciado.")
    while True:
        train_model()
        print(f"⏳ Próximo treinamento agendado para ~{(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M')}")
        time.sleep(7 * 24 * 3600)

if __name__ == "__main__":
    main()