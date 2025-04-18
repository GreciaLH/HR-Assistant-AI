from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.router import api_router
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplazar con orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir el API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Crear directorio de subida si no existe
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to Resume Ranking API"}

@app.get("/init-db")
async def initialize_database():
    Base.metadata.create_all(bind=engine)
    return {"message": "Database initialized successfully"}