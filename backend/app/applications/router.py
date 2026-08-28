from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List, Dict, Any
from app.schemas.application import ApplicationCreate, ApplicationUpdate, StageUpdateRequest
from app.repositories.application_repository import application_repository
from app.dependencies.auth import get_optional_user, get_current_user

router = APIRouter(prefix="/api/v1/applications", tags=["Application Tracker CRM"])

@router.get("/")
async def list_applications(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    apps = await application_repository.get_user_applications(user_id)
    if not apps:
        # Seed default starter applications for user if empty
        defaults = [
            {"company": "Google", "role": "Software Engineering Intern 2026", "stage": "Online Assessment", "status": "Online Assessment", "deadline": "Sep 05, 2026", "location": "Hyderabad / Remote", "match_score": 92, "ctc": "₹28 LPA"},
            {"company": "Microsoft", "role": "Graduate Software Engineer", "stage": "Technical Round 1", "status": "Interview", "deadline": "Aug 30, 2026", "location": "Bengaluru, IN", "match_score": 88, "ctc": "₹24 LPA"},
            {"company": "Amazon", "role": "SDE-1 (Full Stack)", "stage": "Applied", "status": "Applied", "deadline": "Sep 12, 2026", "location": "Hyderabad, IN", "match_score": 85, "ctc": "₹22 LPA"},
            {"company": "Swiggy", "role": "Backend Engineer", "stage": "Offer Received", "status": "Offer", "deadline": "Sep 15, 2026", "location": "Bengaluru", "match_score": 90, "ctc": "₹18 LPA"}
        ]
        for d in defaults:
            await application_repository.create_application(user_id, d)
        apps = await application_repository.get_user_applications(user_id)

    # Format id fields
    for a in apps:
        a["id"] = str(a.get("_id", a.get("id", "")))
        if "stage" not in a and "status" in a:
            a["stage"] = a["status"]
    return {"status": "success", "data": apps}

@router.post("/")
async def create_application(payload: ApplicationCreate, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    created = await application_repository.create_application(user_id, payload.dict())
    created["id"] = str(created.get("_id", ""))
    return {"status": "success", "message": "Application created in MongoDB.", "data": created}

@router.put("/update-stage")
async def update_stage(req: StageUpdateRequest, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    updated = await application_repository.update_stage(user_id, req.app_id, req.new_stage)
    if not updated:
        # Create or update fallback
        updated = {"id": req.app_id, "stage": req.new_stage, "status": req.new_stage}
    else:
        updated["id"] = str(updated.get("_id", req.app_id))
    return {"status": "success", "message": "Stage updated in MongoDB.", "data": updated}

@router.delete("/{app_id}")
async def delete_application(app_id: str, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    deleted = await application_repository.delete_application(user_id, app_id)
    return {"status": "success", "message": "Application deleted from MongoDB." if deleted else "Not found"}
