from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, Dict, Any
from app.services.weakness_detector_service import WeaknessDetectorService
from app.repositories.weakness_repository import weakness_repository
from app.dependencies.auth import get_optional_user

router = APIRouter(prefix="/api/v1/weakness", tags=["AI Weakness Detector"])

@router.get("/analysis")
async def get_weakness_analysis(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    latest = await weakness_repository.get_latest_by_user_id(user_id)
    if not latest:
        latest = await WeaknessDetectorService.analyze_user_weaknesses(user_id)
    return {
        "status": "success",
        "analysis": latest
    }

@router.post("/analyze")
async def trigger_weakness_analysis(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    fresh_analysis = await WeaknessDetectorService.analyze_user_weaknesses(user_id)
    return {
        "status": "success",
        "message": "AI Weakness Analysis recalculated based on actual platform performance metrics.",
        "analysis": fresh_analysis
    }
