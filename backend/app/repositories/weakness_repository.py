from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager

class WeaknessRepository:
    def __init__(self):
        self.collection_name = "user_weakness_analyses"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def get_latest_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.col.find_one({"user_id": str(user_id)}, sort=[("created_at", -1)])
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def save_analysis(self, user_id: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = dict(analysis_data)
        doc["user_id"] = str(user_id)
        doc["created_at"] = now
        doc["updated_at"] = now

        res = await self.col.insert_one(doc)
        if hasattr(res, "inserted_id"):
            doc["_id"] = str(res.inserted_id)
            doc["id"] = str(res.inserted_id)
        return doc

weakness_repository = WeaknessRepository()
