from fastapi import APIRouter, Depends
from typing import Optional, Dict, Any
from app.repositories.notification_repository import notification_repository
from app.dependencies.auth import get_optional_user

router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications"])

@router.get("/")
async def get_notifications(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    notifs = await notification_repository.get_user_notifications(user_id)
    for n in notifs:
        n["id"] = str(n.get("_id", n.get("id", "")))
    return {"status": "success", "notifications": notifs}

@router.put("/{notif_id}/read")
async def mark_read(notif_id: str, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    await notification_repository.mark_read(user_id, notif_id)
    return {"status": "success", "message": "Notification marked as read in MongoDB."}

@router.put("/read-all")
async def mark_all_read(user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    await notification_repository.mark_all_read(user_id)
    return {"status": "success", "message": "All notifications marked as read."}

@router.delete("/{notif_id}")
async def delete_notification(notif_id: str, user: Optional[Dict[str, Any]] = Depends(get_optional_user)):
    user_id = str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    await notification_repository.delete_notification(user_id, notif_id)
    return {"status": "success", "message": "Notification deleted."}
