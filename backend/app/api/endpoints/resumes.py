from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from ...db.session import get_db
from ...schemas import resume as schemas
from ...services import resume_service as service

router = APIRouter()

@router.post("/", response_model=schemas.Resume, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return await service.create_resume_from_file(db=db, file=file)

@router.get("/", response_model=List[schemas.Resume])
def read_resumes(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return service.get_resumes(db=db, skip=skip, limit=limit)

@router.get("/{resume_id}", response_model=schemas.Resume)
def read_resume(
    resume_id: int, 
    db: Session = Depends(get_db)
):
    db_resume = service.get_resume(db=db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return db_resume

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: int, 
    db: Session = Depends(get_db)
):
    db_resume = service.get_resume(db=db, resume_id=resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    service.delete_resume(db=db, resume_id=resume_id)
    return None