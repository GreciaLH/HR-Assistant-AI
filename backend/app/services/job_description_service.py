from sqlalchemy.orm import Session
from ..models.job_description import JobDescription
from ..schemas.job_description import JobDescriptionCreate, JobDescriptionUpdate
import json
from ..core.config import settings

# Comentamos temporalmente las importaciones de LangChain
# from langchain.llms import OpenAI
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

def get_job_description(db: Session, job_id: int):
    return db.query(JobDescription).filter(JobDescription.id == job_id).first()

def get_job_descriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(JobDescription).offset(skip).limit(limit).all()

def create_job_description(db: Session, job_desc: JobDescriptionCreate):
    # Extract structured data using a simplified method for now
    structured_data = extract_job_description_data(job_desc.description)
    
    # Create new job description
    db_job = JobDescription(
        title=job_desc.title,
        company=job_desc.company,
        description=job_desc.description,
        requirements=structured_data.get("requirements", ""),
        skills=json.dumps(structured_data.get("skills", [])),
        location=job_desc.location
    )
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job_description(db: Session, job_id: int, job_desc: JobDescriptionUpdate):
    db_job = get_job_description(db, job_id)
    
    # Update fields if provided
    if job_desc.title is not None:
        db_job.title = job_desc.title
    if job_desc.company is not None:
        db_job.company = job_desc.company
    if job_desc.description is not None:
        db_job.description = job_desc.description
        # Re-extract structured data
        structured_data = extract_job_description_data(job_desc.description)
        db_job.requirements = structured_data.get("requirements", "")
        db_job.skills = json.dumps(structured_data.get("skills", []))
    if job_desc.requirements is not None:
        db_job.requirements = job_desc.requirements
    if job_desc.skills is not None:
        db_job.skills = job_desc.skills
    if job_desc.location is not None:
        db_job.location = job_desc.location
    
    db.commit()
    db.refresh(db_job)
    return db_job

def delete_job_description(db: Session, job_id: int):
    db_job = get_job_description(db, job_id)
    db.delete(db_job)
    db.commit()
    return db_job

def extract_job_description_data(description: str):
    """
    Extract structured data from job description - simplified version
    """
    # Simplified version that doesn't use LangChain
    return {
        "requirements": "Requirements extracted from description",
        "skills": ["Python", "FastAPI", "SQL", "Docker"]
    }
    
    prompt_template = PromptTemplate(
        input_variables=["description"],
        template="""
        Extract the key requirements and skills from the following job description:
        
        {description}
        
        Return the data in the following JSON format:
        {{
            "requirements": "A paragraph summarizing the key requirements",
            "skills": ["skill1", "skill2", "skill3", ...]
        }}
        """
    )
    
    llm = OpenAI(temperature=0, api_key=settings.OPENAI_API_KEY)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    try:
        result = chain.run(description=description)
        return json.loads(result)
    except Exception as e:
        print(f"Error extracting job description data: {e}")
        return {
            "requirements": "Failed to extract requirements",
            "skills": []
        }