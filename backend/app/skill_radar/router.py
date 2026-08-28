from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, Dict, Any, List
from app.services.skill_radar_service import SkillRadarService, ROLE_TARGET_BENCHMARKS
from app.dependencies.auth import get_optional_user, resolve_user_id

router = APIRouter(prefix="/api/v1/skill-radar", tags=["Career Skill Radar"])

@router.get("/radar")
async def get_skill_radar(
    target_role: Optional[str] = Query("Software Engineer"),
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = resolve_user_id(user)
    snapshot = await SkillRadarService.compute_skill_radar(user_id, target_role or "Software Engineer")
    return {
        "status": "success",
        "radar": snapshot
    }

@router.get("/targets")
async def get_target_role_benchmarks():
    return {
        "status": "success",
        "roles": list(ROLE_TARGET_BENCHMARKS.keys()),
        "benchmarks": ROLE_TARGET_BENCHMARKS
    }

@router.get("/history")
async def get_radar_history(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    history = await SkillRadarService.get_radar_history(user_id)
    return {
        "status": "success",
        "history": history
    }
