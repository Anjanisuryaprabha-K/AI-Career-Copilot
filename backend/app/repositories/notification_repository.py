from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager

DEFAULT_USER_NOTIFICATIONS = [
    {
        "title": "Google Placement Assessment Scheduled",
        "message": "Online coding assessment round is scheduled for Sep 5, 2026.",
        "type": "assessment",
        "read": False
    },
    {
        "title": "ATS Resume Score Improved to 88%",
        "message": "Your latest resume scan scored in the top 12% of candidates.",
        "type": "resume",
        "read": False
    },
    {
        "title": "Microsoft Placement Drive Live",
        "message": "New SDE-1 graduate openings posted. Check Job Matcher for your fit score.",
        "type": "job",
        "read": True
    }
]

class NotificationRepository:
    def __init__(self):
        self.collection_name = "notifications"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def get_user_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        items = await self.col.find({"user_id": str(user_id)}).sort("created_at", -1).to_list(50)
        if not items:
            now = datetime.utcnow().isoformat()
            for notif in DEFAULT_USER_NOTIFICATIONS:
                doc = dict(notif)
                doc["user_id"] = str(user_id)
                doc["created_at"] = now
                await self.col.insert_one(doc)
            items = await self.col.find({"user_id": str(user_id)}).sort("created_at", -1).to_list(50)
        return items

    async def mark_read(self, user_id: str, notif_id: str) -> bool:
        await self.col.update_one({"_id": notif_id, "user_id": str(user_id)}, {"$set": {"read": True}})
        await self.col.update_one({"id": notif_id, "user_id": str(user_id)}, {"$set": {"read": True}})
        return True

    async def mark_all_read(self, user_id: str) -> bool:
        cursor = self.col.find({"user_id": str(user_id)})
        items = await cursor.to_list(100)
        for it in items:
            await self.col.update_one({"_id": it["_id"]}, {"$set": {"read": True}})
        return True

    async def delete_notification(self, user_id: str, notif_id: str) -> bool:
        return await self.col.delete_one({"_id": notif_id, "user_id": str(user_id)}) or await self.col.delete_one({"id": notif_id, "user_id": str(user_id)})

notification_repository = NotificationRepository()
