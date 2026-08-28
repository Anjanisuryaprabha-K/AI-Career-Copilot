from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.cover_letter_service import CoverLetterService
from app.dependencies.auth import get_optional_user, resolve_user_id
from app.repositories.content_repository import cover_letter_repository

router = APIRouter(prefix="/api/v1/cover-letter", tags=["Cover Letter Generator"])

class CoverLetterRequest(BaseModel):
    user_name: str = "Candidate"
    target_role: str = "Software Engineer"
    company_name: str = "Tech Corp"
    skills: Optional[List[str]] = ["Python", "FastAPI", "React", "MongoDB"]
    experience_summary: Optional[str] = "I have developed full-stack scalable web applications and solved 300+ LeetCode algorithmic challenges."

@router.post("/generate")
async def generate_cover_letter(req: CoverLetterRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    res = CoverLetterService.generate_cover_letter(
        user_name=req.user_name,
        target_role=req.target_role,
        company_name=req.company_name,
        skills=req.skills,
        experience_summary=req.experience_summary
    )
    if user:
        user_id = resolve_user_id(user)
        await cover_letter_repository.save(user_id, req.target_role, req.company_name, res)
    return res
