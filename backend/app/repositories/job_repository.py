from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager

class JobRepository:
    def __init__(self):
        self.matches_col_name = "job_matches"
        self.searches_col_name = "job_searches"
        self.salary_col_name = "salary_predictions"

    @property
    def matches_col(self):
        return db_manager.get_collection(self.matches_col_name)

    @property
    def salary_col(self):
        return db_manager.get_collection(self.salary_col_name)

    async def save_user_job_matches(self, user_id: str, matches: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        now = datetime.utcnow().isoformat()
        # Clean previous matches and save new
        await self.matches_col.delete_many({"user_id": str(user_id)})
        for m in matches:
            doc = dict(m)
            doc["user_id"] = str(user_id)
            doc["created_at"] = now
            doc["saved"] = False
            await self.matches_col.insert_one(doc)
        return await self.matches_col.find({"user_id": str(user_id)}).to_list(50)

    async def get_user_jobs(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.matches_col.find({"user_id": str(user_id)}).sort("match_score", -1).to_list(50)

    async def toggle_save_job(self, user_id: str, job_id: str, saved: bool) -> bool:
        await self.matches_col.update_one(
            {"_id": job_id, "user_id": str(user_id)},
            {"$set": {"saved": saved, "updated_at": datetime.utcnow().isoformat()}}
        )
        return True

    async def save_salary_prediction(self, user_id: str, payload: Dict[str, Any], prediction: Dict[str, Any], sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = {
            "user_id": str(user_id),
            "input_parameters": payload,
            "prediction": prediction,
            "data_sources": sources,
            "created_at": now
        }
        res = await self.salary_col.insert_one(doc)
        if hasattr(res, "inserted_id"):
            doc["_id"] = str(res.inserted_id)
        return doc

job_repository = JobRepository()
