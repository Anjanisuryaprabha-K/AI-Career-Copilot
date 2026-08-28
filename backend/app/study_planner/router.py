from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.services.study_planner_service import StudyPlannerService
from app.dependencies.auth import get_optional_user, resolve_user_id

router = APIRouter(prefix="/api/v1/study-planner", tags=["AI Study Planner"])

class GeneratePlanRequest(BaseModel):
    target_role: str = "Software Engineer"
    target_company: Optional[str] = None
    interview_date: Optional[str] = None
    available_hours_per_day: int = 2
    days_per_week: int = 5
    preferred_study_time: str = "Evening"
    current_skill_level: str = "Intermediate"

class CompleteTaskRequest(BaseModel):
    task_id: str

@router.get("/plan")
async def get_study_plan(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    plan = await StudyPlannerService.get_user_study_plan(user_id)
    return {
        "status": "success",
        "plan": plan
    }

@router.post("/generate")
async def generate_study_plan(
    payload: GeneratePlanRequest,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = resolve_user_id(user)
    plan = await StudyPlannerService.generate_study_plan(user_id, payload.dict())
    return {
        "status": "success",
        "plan": plan
    }

@router.post("/complete-task")
async def complete_task(
    payload: CompleteTaskRequest,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = resolve_user_id(user)
    res = await StudyPlannerService.complete_task(user_id, payload.task_id)
    return res

@router.post("/reschedule")
async def reschedule_missed_tasks(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = resolve_user_id(user)
    res = await StudyPlannerService.reschedule_missed_tasks(user_id)
    return res
