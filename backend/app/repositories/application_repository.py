from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager

class ApplicationRepository:
    def __init__(self):
        self.collection_name = "applications"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def get_user_applications(self, user_id: str) -> List[Dict[str, Any]]:
        cursor = self.col.find({"user_id": str(user_id)}).sort("created_at", -1)
        return await cursor.to_list(100)

    async def create_application(self, user_id: str, app_data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = dict(app_data)
        doc["user_id"] = str(user_id)
        if "created_at" not in doc:
            doc["created_at"] = now
        if "updated_at" not in doc:
            doc["updated_at"] = now
        if "status" not in doc:
            doc["status"] = "Applied"
        res = await self.col.insert_one(doc)
        if hasattr(res, "inserted_id"):
            doc["_id"] = str(res.inserted_id)
            doc["id"] = str(res.inserted_id)
        return doc

    async def update_stage(self, user_id: str, app_id: str, new_stage: str) -> Optional[Dict[str, Any]]:
        now = datetime.utcnow().isoformat()
        # Enforce user isolation: user_id must match
        filter_dict = {"_id": app_id, "user_id": str(user_id)}
        update_dict = {"$set": {"status": new_stage, "stage": new_stage, "updated_at": now}}
        await self.col.update_one(filter_dict, update_dict)
        
        # Also try matching on "id" field
        filter_dict_id = {"id": app_id, "user_id": str(user_id)}
        await self.col.update_one(filter_dict_id, update_dict)
        
        return await self.col.find_one({"_id": app_id, "user_id": str(user_id)}) or await self.col.find_one({"id": app_id, "user_id": str(user_id)})

    async def update_application(self, user_id: str, app_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        updates["updated_at"] = datetime.utcnow().isoformat()
        filter_dict = {"_id": app_id, "user_id": str(user_id)}
        await self.col.update_one(filter_dict, {"$set": updates})
        return await self.col.find_one(filter_dict)

    async def delete_application(self, user_id: str, app_id: str) -> bool:
        return await self.col.delete_one({"_id": app_id, "user_id": str(user_id)}) or await self.col.delete_one({"id": app_id, "user_id": str(user_id)})

application_repository = ApplicationRepository()
