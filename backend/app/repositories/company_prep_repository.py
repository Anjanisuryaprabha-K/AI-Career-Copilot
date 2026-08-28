from datetime import datetime
from typing import Optional, Dict, Any
from app.database.mongodb import db_manager

class CompanyPrepRepository:
    def __init__(self):
        self.collection_name = "user_company_prep"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def get_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.col.find_one({"user_id": str(user_id)}, sort=[("updated_at", -1)])
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def save_prep_selection(self, user_id: str, company_id: str, target_role: str, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = {
            "user_id": str(user_id),
            "company_id": str(company_id),
            "target_role": str(target_role),
            "plan_data": plan_data,
            "updated_at": now
        }

        res = await self.col.update_one(
            {"user_id": str(user_id)},
            {"$set": doc},
            upsert=True
        )

        saved = await self.get_by_user_id(user_id)
        return saved or doc

company_prep_repository = CompanyPrepRepository()
