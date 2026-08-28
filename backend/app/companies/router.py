from fastapi import APIRouter, HTTPException
from app.services.google_search_service import GoogleSearchService
from app.services.company_service import CompanyService
from app.repositories.content_repository import company_insights_repository

router = APIRouter(prefix="/api/v1/companies", tags=["Company Insights & Hiring Trends"])

@router.get("/")
async def list_companies():
    return {"status": "success", "companies": CompanyService.get_all_companies()}

@router.get("/{comp_id}")
async def get_company_details(comp_id: str):
    data = await GoogleSearchService.get_company_insights(comp_id)
    # Cache insight data via repository (best-effort, errors swallowed internally)
    await company_insights_repository.upsert_insights(comp_id, data)
    return {"status": "success", "company": data}
