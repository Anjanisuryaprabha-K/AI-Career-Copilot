from fastapi import APIRouter, Depends
from typing import Optional, Dict, Any
from app.repositories.analytics_repository import analytics_repository
from app.dependencies.auth import get_optional_user

router = APIRouter(prefix="/api/v1/analytics", tags=["Real-Time Placement Analytics"])

@router.get("/summary")
async def get_analytics_summary(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    summary = await analytics_repository.compute_user_analytics(user_id)
    return {"status": "success", "data": summary}
