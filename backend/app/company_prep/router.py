from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.company_prep_service import CompanyPrepService
from app.repositories.company_prep_repository import company_prep_repository
from app.dependencies.auth import get_optional_user

router = APIRouter(prefix="/api/v1/company-prep", tags=["Company-Specific Preparation"])

class SelectCompanyPrepRequest(BaseModel):
    company_id: str
    target_role: Optional[str] = None

@router.get("/catalog")
async def get_company_catalog():
    return {
        "status": "success",
        "companies": CompanyPrepService.get_catalog()
    }

@router.get("/plan")
async def get_company_prep_plan(
    company_id: Optional[str] = "ibm",
    target_role: Optional[str] = None,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    plan = await CompanyPrepService.get_company_prep_plan(user_id, company_id, target_role)
    return {
        "status": "success",
        "plan": plan
    }

@router.post("/select")
async def select_company_prep(
    payload: SelectCompanyPrepRequest,
    user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    plan = await CompanyPrepService.get_company_prep_plan(user_id, payload.company_id, payload.target_role)
    return {
        "status": "success",
        "message": f"Company preparation target set to '{plan['company']['name']}' ({plan['target_role']})",
        "plan": plan
    }
