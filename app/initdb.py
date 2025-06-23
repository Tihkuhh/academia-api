from app.database import engine, Base
from app import models  # importa os modelos para que o SQLAlchemy os registre

def init_db():
    print("🔧 Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

if __name__ == "__main__":
    init_db()
