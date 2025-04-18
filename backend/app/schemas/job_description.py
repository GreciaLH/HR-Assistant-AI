from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobDescriptionBase(BaseModel):
    title: str
    company: str
    description: str
    requirements: Optional[str] = None
    skills: Optional[str] = None
    location: Optional[str] = None

class JobDescriptionCreate(JobDescriptionBase):
    pass

class JobDescriptionUpdate(JobDescriptionBase):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None

class JobDescription(JobDescriptionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True