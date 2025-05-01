from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...db.session import get_db
from ...schemas import job_description as schemas
from ...services import job_description_service as service

router = APIRouter()

@router.post("/", response_model=schemas.JobDescription, status_code=status.HTTP_201_CREATED)
def create_job_description(
    job_desc: schemas.JobDescriptionCreate, 
    db: Session = Depends(get_db)
):
    return service.create_job_description(db=db, job_desc=job_desc)

@router.get("/", response_model=List[schemas.JobDescription])
def read_job_descriptions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return service.get_job_descriptions(db=db, skip=skip, limit=limit)

@router.get("/{job_id}", response_model=schemas.JobDescription)
def read_job_description(
    job_id: int, 
    db: Session = Depends(get_db)
):
    db_job = service.get_job_description(db=db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    return db_job

@router.put("/{job_id}", response_model=schemas.JobDescription)
def update_job_description(
    job_id: int, 
    job_desc: schemas.JobDescriptionUpdate, 
    db: Session = Depends(get_db)
):
    db_job = service.get_job_description(db=db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    return service.update_job_description(db=db, job_id=job_id, job_desc=job_desc)

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_description(
    job_id: int, 
    db: Session = Depends(get_db)
):
    db_job = service.get_job_description(db=db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    service.delete_job_description(db=db, job_id=job_id)
    return None