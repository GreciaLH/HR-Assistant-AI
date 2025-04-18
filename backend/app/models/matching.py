from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from ..db.base import Base

class Matching(Base):
    __tablename__ = "matchings"

    id = Column(Integer, primary_key=True, index=True)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    score = Column(Float, nullable=False)  # Puntuación general de coincidencia (0-100)
    comments = Column(Text, nullable=True)  # Comentarios generales sobre la coincidencia
    analysis = Column(Text, nullable=True)  # Análisis detallado (almacenado como JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relaciones
    job_description = relationship("JobDescription", back_populates="matches")
    resume = relationship("Resume", back_populates="matches")