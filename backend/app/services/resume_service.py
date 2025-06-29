from sqlalchemy.orm import Session
from fastapi import UploadFile
import os
import json
from ..models.resume import Resume
from ..schemas.resume import ResumeCreate
from ..core.config import settings
from ..utils.file_handler import save_upload_file, extract_text_from_file
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

async def create_resume_from_file(db: Session, file: UploadFile):
    """
    Create a resume by extracting all information from the uploaded file
    """
    # guardar el archivo en la carpeta de subida
    file_path = await save_upload_file(file, settings.UPLOAD_FOLDER)
    
    # Extraer texto del archivo
    content = await extract_text_from_file(file_path)
    
    # Extraer datos estructurados del currículum usando LangChain/GPT
    structured_data = extract_resume_data(content)
    
    # Extrae información del candidato del currículum
    candidate_info = extract_candidate_info(content)
    
    # Crear el objeto de Resume
    db_resume = Resume(
        candidate_name=candidate_info.get("name", "Unknown"),
        email=candidate_info.get("email", None),
        phone=candidate_info.get("phone", None),
        file_path=file_path,
        content=content,
        skills=json.dumps(structured_data.get("skills", [])),
        experience=json.dumps(structured_data.get("experience", [])),
        education=json.dumps(structured_data.get("education", []))
    )
    
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume



def get_resume(db: Session, resume_id: int):
    return db.query(Resume).filter(Resume.id == resume_id).first()

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Resume).offset(skip).limit(limit).all()

def delete_resume(db: Session, resume_id: int):
    db_resume = get_resume(db, resume_id)
    
    # Borrar el archivo si  existe
    if db_resume and os.path.exists(db_resume.file_path):
        os.remove(db_resume.file_path)
    
    db.delete(db_resume)
    db.commit()
    return db_resume

def extract_resume_data(content: str):
    """
    Extract structured data from resume content using LangChain/GPT
    """
    # Esto es un marcador de posición. En una implementación real, usarías LangChain y GPT
    # para extraer datos estructurados del currículum.
    
    # Ejemplo de implentación:
    if not settings.OPENAI_API_KEY:
        # Si no hay API key, devolver datos de ejemplo
        return {
            "skills": [],
            "experience": [],
            "education": []
        }
    
    prompt = f"""
    Extract structured data from the following resume:
    
    {content}
    
    Return only the data in the following JSON format:
    {{
        "skills": ["skill1", "skill2", ...],
        "experience": [
            {{
                "title": "Job Title",
                "company": "Company Name",
                "duration": "Duration",
                "description": "Brief description"
            }},
            ...
        ],
        "education": [
            {{
                "degree": "Degree Name",
                "institution": "Institution Name",
                "year": "Year"
            }},
            ...
        ]
    }}
    """
    
    # Inicializar el modelo de chat de OpenAI para procesar el texto del currículum
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=settings.OPENAI_API_KEY)
    
    try:
        # Procesar el texto del currículum
        messages = [HumanMessage(content=prompt)]
        result = chat(messages).content
        return json.loads(result)
    except Exception as e:
        print(f"Error extracting resume data: {e}")
        return {
            "skills": [],
            "experience": [],
            "education": []
        }

def extract_candidate_info(content: str):
    """
    Extract candidate name, email and phone from resume content
    """
    if not settings.OPENAI_API_KEY:
        # si no hay API key, devolver datos de ejemplo
        return {
            "name": "Candidate Name",
            "email": "candidate@example.com",
            "phone": "123-456-7890"
        }
    
    prompt = f"""
    Extract the candidate's basic information from the following resume:
    
    {content}
    
    Return only the data in the following JSON format:
    {{
        "name": "Full Name",
        "email": "email@example.com",
        "phone": "Phone Number"
    }}
    """
    
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=settings.OPENAI_API_KEY)
    
    try:
        # Procesar el texto del currículum
        messages = [HumanMessage(content=prompt)]
        result = chat(messages).content
        return json.loads(result)
    except Exception as e:
        print(f"Error extracting candidate info: {e}")
        return {
            "name": "Unknown Candidate",
            "email": None,
            "phone": None
        }