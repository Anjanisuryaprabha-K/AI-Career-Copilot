from typing import Optional, Dict, Any, List
from datetime import datetime
from app.database.mongodb import db_manager

class StudyPlannerRepository:
    def __init__(self):
        self._in_memory_db: Dict[str, Dict[str, Any]] = {}

    def _get_collection(self):
        try:
            return db_manager.get_collection("user_study_plans")
        except Exception:
            return None

    async def save_user_plan(self, user_id: str, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        user_id_str = str(user_id)
        coll = self._get_collection()

        doc = {
            "user_id": user_id_str,
            "target_role": plan_data.get("target_role", "Software Engineer"),
            "target_company": plan_data.get("target_company"),
            "interview_date": plan_data.get("interview_date"),
            "available_hours_per_day": plan_data.get("available_hours_per_day", 2),
            "days_per_week": plan_data.get("days_per_week", 5),
            "preferred_study_time": plan_data.get("preferred_study_time", "Evening"),
            "current_skill_level": plan_data.get("current_skill_level", "Intermediate"),
            "days_schedule": plan_data.get("days_schedule", []),
            "total_tasks_count": plan_data.get("total_tasks_count", 0),
            "completed_tasks_count": plan_data.get("completed_tasks_count", 0),
            "completion_percentage": plan_data.get("completion_percentage", 0.0),
            "current_focus": plan_data.get("current_focus", "DSA & Resume Optimization"),
            "updated_at": datetime.utcnow().isoformat()
        }

        if coll is not None:
            await coll.update_one({"user_id": user_id_str}, {"$set": doc}, upsert=True)
        else:
            self._in_memory_db[user_id_str] = doc

        return doc

    async def get_user_plan(self, user_id: str) -> Optional[Dict[str, Any]]:
        user_id_str = str(user_id)
        coll = self._get_collection()

        if coll is not None:
            doc = await coll.find_one({"user_id": user_id_str})
            if doc:
                doc["_id"] = str(doc["_id"])
                return doc
            return None

        return self._in_memory_db.get(user_id_str)

study_planner_repository = StudyPlannerRepository()
