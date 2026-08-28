from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.linkedin_service import LinkedInService
from app.dependencies.auth import get_optional_user, resolve_user_id
from app.repositories.content_repository import linkedin_repository

router = APIRouter(prefix="/api/v1/linkedin", tags=["LinkedIn Optimizer"])

class LinkedInOptimizeRequest(BaseModel):
    target_role: str = "Software Engineer"
    skills: Optional[List[str]] = ["Python", "React", "Data Structures", "FastAPI"]
    experience_level: Optional[str] = "Student / Placement Aspirant"

@router.post("/optimize")
async def optimize_profile(req: LinkedInOptimizeRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    res = LinkedInService.optimize_profile(
        target_role=req.target_role,
        current_skills=req.skills or [],
        experience_level=req.experience_level or ""
    )
    if user:
        user_id = resolve_user_id(user)
        await linkedin_repository.save(user_id, req.target_role, req.skills or [], res)
    return res
