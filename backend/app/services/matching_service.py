from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from ..models.matching import Matching
from ..models.job_description import JobDescription
from ..models.resume import Resume
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from ..core.config import settings

def create_matching(db: Session, job_id: int, resume_ids: List[int]):
    # Get job description
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise ValueError(f"Job description with ID {job_id} not found")
    
    results = []
    
    for resume_id in resume_ids:
        # Get resume
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            continue  # Skip if resume not found
        
        # Check if matching already exists
        existing_match = db.query(Matching).filter(
            Matching.job_description_id == job_id,
            Matching.resume_id == resume_id
        ).first()
        
        if existing_match:
            # Update existing match
            match_result = perform_matching(job, resume)
            existing_match.score = match_result.score
            existing_match.comments = match_result.comments
            db.commit()
            db.refresh(existing_match)
            results.append(existing_match)
        else:
            # Create new match
            match_result = perform_matching(job, resume)
            db_match = Matching(
                job_description_id=job_id,
                resume_id=resume_id,
                score=match_result.score,
                comments=match_result.comments
            )
            db.add(db_match)
            db.commit()
            db.refresh(db_match)
            results.append(db_match)
    
    return results

def get_matching(db: Session, matching_id: int):
    return db.query(Matching).filter(Matching.id == matching_id).first()

def get_matchings_by_job(db: Session, job_id: int):
    # Get all matchings for the job
    matchings = db.query(Matching).filter(Matching.job_description_id == job_id).all()
    
    # Filter out any invalid matchings (those with None resume_id)
    valid_matchings = [m for m in matchings if m.resume_id is not None]
    
    return valid_matchings

def get_matchings_by_resume(db: Session, resume_id: int):
    return db.query(Matching).filter(Matching.resume_id == resume_id).all()

def perform_matching(job: JobDescription, resume: Resume) -> Matching:
    """
    Perform matching between job description and resume using LangChain/GPT
    """
    if not job or not resume:
        print("Error: Job or resume is None")
        return None
        
    # Replace the prompt template and OpenAI model with ChatOpenAI
    prompt = f"""
    Compara la siguiente descripción de trabajo y currículum, y evalúa qué tan bien coincide el candidato con los requisitos del trabajo:

    DESCRIPCIÓN DEL TRABAJO:
    Título: {job.title}
    Empresa: {job.company}
    Requisitos: {job.requirements if job.requirements else ""}
    Habilidades: {job.skills if job.skills else ""}

    CURRÍCULUM:
    Candidato: {resume.candidate_name}
    Habilidades: {resume.skills if resume.skills else ""}
    Experiencia: {resume.experience if resume.experience else ""}
    Educación: {resume.education if resume.education else ""}
    Contenido: {resume.content if resume.content else ""}

    Proporciona una puntuación de coincidencia del 0-100 y comentarios detallados sobre la coincidencia en el siguiente formato JSON:
    {{
        "score": 85,
        "comments": "Análisis detallado de la coincidencia entre el candidato y los requisitos del trabajo. IMPORTANTE: ESCRIBE ESTE ANÁLISIS COMPLETAMENTE EN ESPAÑOL."
    }}
    """
    
    # Use ChatOpenAI instead of OpenAI
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=settings.OPENAI_API_KEY)
    
    try:
        # Use chat directly instead of chain
        messages = [HumanMessage(content=prompt)]
        result = chat(messages).content
        matching_result = json.loads(result)
        
        # Create new matching object with all required fields
        db_matching = Matching(
            job_description_id=job.id,
            resume_id=resume.id,
            score=matching_result.get("score", 0),
            comments=matching_result.get("comments", "")
        )
        
        return db_matching
    except Exception as e:
        print(f"Error performing matching: {e}")
        # Return a default matching with a low score
        return Matching(
            job_description_id=job.id,
            resume_id=resume.id,
            score=0,
            comments=f"Error al realizar la coincidencia: {str(e)}"
        )