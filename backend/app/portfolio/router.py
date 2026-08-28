from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.portfolio_service import PortfolioService
from app.dependencies.auth import get_optional_user, resolve_user_id
from app.repositories.content_repository import portfolio_repository

router = APIRouter(prefix="/api/v1/portfolio", tags=["Portfolio Builder"])

class PortfolioRequest(BaseModel):
    user_name: str = "Preetham V"
    target_role: str = "Software Engineer"
    bio: Optional[str] = ""
    skills: Optional[List[str]] = []
    projects: Optional[List[dict]] = []

@router.post("/generate")
async def generate_portfolio(req: PortfolioRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    res = PortfolioService.get_portfolio_template(
        user_name=req.user_name,
        target_role=req.target_role,
        bio=req.bio or "",
        skills=req.skills or [],
        projects=req.projects or []
    )
    if user:
        user_id = resolve_user_id(user)
        await portfolio_repository.upsert(user_id, req.target_role, res)
    return res
