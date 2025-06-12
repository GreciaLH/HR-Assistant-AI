from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
import datetime
from ..db.base import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    file_path = Column(String(255), nullable=False)  # Path to the stored resume file
    content = Column(Text, nullable=True)  # Extracted text content
    skills = Column(Text, nullable=True)  # Stored as JSON string
    experience = Column(Text, nullable=True)  # Stored as JSON string
    education = Column(Text, nullable=True)  # Stored as JSON string
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relaciones
    matches = relationship("Matching", back_populates="resume")