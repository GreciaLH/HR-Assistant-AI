from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResumeBase(BaseModel):
    candidate_name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class ResumeCreate(ResumeBase):
    file_path: str
    content: Optional[str] = None

class Resume(ResumeBase):
    id: int
    file_path: str
    content: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True