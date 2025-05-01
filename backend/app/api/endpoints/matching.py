from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...db.session import get_db
from ...schemas import matching as schemas
from ...services import matching_service as service

router = APIRouter()

@router.post("/", response_model=List[schemas.Matching], status_code=status.HTTP_201_CREATED)
def create_matching(
    matching_request: schemas.MatchingRequest, 
    db: Session = Depends(get_db)
):
    return service.create_matching(db=db, job_id=matching_request.job_description_id, resume_ids=matching_request.resume_ids)

@router.get("/job/{job_id}", response_model=List[schemas.Matching])
def read_matchings_by_job(
    job_id: int, 
    db: Session = Depends(get_db)
):
    return service.get_matchings_by_job(db=db, job_id=job_id)

@router.get("/resume/{resume_id}", response_model=List[schemas.Matching])
def read_matchings_by_resume(
    resume_id: int, 
    db: Session = Depends(get_db)
):
    return service.get_matchings_by_resume(db=db, resume_id=resume_id)

@router.get("/{matching_id}", response_model=schemas.Matching)
def read_matching(
    matching_id: int, 
    db: Session = Depends(get_db)
):
    db_matching = service.get_matching(db=db, matching_id=matching_id)
    if db_matching is None:
        raise HTTPException(status_code=404, detail="Matching not found")
    return db_matching