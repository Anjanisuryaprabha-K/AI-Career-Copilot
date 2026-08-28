from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.google_search_service import GoogleSearchService

router = APIRouter(prefix="/api/v1/search", tags=["Google Search & Live Intelligence"])

@router.get("")
@router.get("/")
async def search_web(
    query: str = Query(..., description="The search term or job requirement"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    type: str = Query("all", description="Search type: all, jobs, companies, salary")
):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
    
    results = await GoogleSearchService.search(
        query=query,
        search_type=type,
        limit=limit,
        page=page
    )
    return results
