from fastapi import APIRouter
from app.services.admin_portal_service import AdminPortalService

router = APIRouter(prefix="/api/v1/admin", tags=["Placement Cell & Recruiter Portal"])

@router.get("/batch-analytics")
async def get_analytics():
    return {"status": "success", "data": AdminPortalService.get_batch_analytics()}
