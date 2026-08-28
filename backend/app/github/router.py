from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.github_scorer import GitHubScorer
from app.dependencies.auth import get_optional_user

router = APIRouter(prefix="/api/v1/github", tags=["GitHub Analyzer"])

class GitHubAnalyzeRequest(BaseModel):
    username: Optional[str] = "preetham-dev"
    github_username: Optional[str] = None

@router.post("/analyze")
@router.post("/score")
async def analyze_github(payload: GitHubAnalyzeRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    uname = (payload.github_username or payload.username or "preetham-dev").strip()
    if not uname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GitHub username cannot be empty."
        )
    user_id = str(user.get("_id", user.get("id"))) if user else None
    result = await GitHubScorer.analyze_profile(uname, user_id=user_id)
    return {"status": "success", "data": result}
