from fastapi import APIRouter
from .endpoints import job_descriptions, resumes, matching

api_router = APIRouter()

api_router.include_router(job_descriptions.router, prefix="/job-descriptions", tags=["job-descriptions"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(matching.router, prefix="/matching", tags=["matching"])