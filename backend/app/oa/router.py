from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.oa_service import OAService

router = APIRouter(prefix="/api/v1/oa", tags=["Mock Online Assessment"])

class OASubmitRequest(BaseModel):
    company: Optional[str] = "Amazon"
    aptitude_score: Optional[int] = 13
    coding_tests_passed: Optional[int] = 6
    total_coding_tests: Optional[int] = 6

@router.get("/config")
async def get_test_config(company: str = "Amazon"):
    return {"status": "success", "data": OAService.get_oa_test_config(company)}

@router.post("/evaluate")
async def evaluate_oa(req: OASubmitRequest):
    return {"status": "success", "data": OAService.evaluate_oa_submission(req.dict())}
