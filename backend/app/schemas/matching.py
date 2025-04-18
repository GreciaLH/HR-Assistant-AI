from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MatchingBase(BaseModel):
    job_description_id: int
    resume_id: int
    score: float
    comments: Optional[str] = None
    analysis: Optional[str] = None

class MatchingCreate(MatchingBase):
    pass

class Matching(MatchingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MatchingRequest(BaseModel):
    job_description_id: int
    resume_ids: List[int]