from datetime import datetime
from typing import Optional, Dict, Any, List
from bson import ObjectId
from app.database.mongodb import db_manager

class GDRepository:
    def __init__(self):
        self.col_name = "user_gd_sessions"

    @property
    def col(self):
        return db_manager.get_collection(self.col_name)

    async def save_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        doc = dict(session_data)
        if "created_at" not in doc:
            doc["created_at"] = datetime.utcnow().isoformat()
        
        res = await self.col.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        doc["id"] = str(res.inserted_id)
        return doc

    async def get_user_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        cursor = self.col.find({"user_id": str(user_id)}).sort("created_at", -1)
        docs = await cursor.to_list(limit)
        for d in docs:
            d["_id"] = str(d.get("_id", ""))
            d["id"] = str(d.get("_id", ""))
        return docs

    async def get_session_by_id(self, user_id: str, session_id: str) -> Optional[Dict[str, Any]]:
        try:
            doc = await self.col.find_one({"_id": ObjectId(session_id), "user_id": str(user_id)})
            if doc:
                doc["_id"] = str(doc["_id"])
                doc["id"] = str(doc["_id"])
            return doc
        except Exception:
            return None

gd_repository = GDRepository()
