import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.base import Base
from app.db.session import engine

# Importar todos los modelos para asegurar que estén registrados con SQLAlchemy
from app.models.job_description import JobDescription
from app.models.resume import Resume
from app.models.matching import Matching

def init_db():
    # Crear todas las tablas en la base de datos
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()