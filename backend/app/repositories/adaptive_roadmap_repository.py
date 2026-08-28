from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager

class AdaptiveRoadmapRepository:
    def __init__(self):
        self.collection_name = "adaptive_roadmaps"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def get_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        doc = await self.col.find_one({"user_id": str(user_id)})
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def save_roadmap(self, user_id: str, roadmap_data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = dict(roadmap_data)
        doc["user_id"] = str(user_id)
        doc["updated_at"] = now
        if "created_at" not in doc:
            doc["created_at"] = now

        await self.col.update_one(
            {"user_id": str(user_id)},
            {"$set": doc},
            upsert=True
        )
        return await self.get_by_user_id(user_id)

    async def toggle_item_status(self, user_id: str, item_id: str, is_completed: Optional[bool] = None) -> Optional[Dict[str, Any]]:
        roadmap = await self.get_by_user_id(user_id)
        if not roadmap:
            return None

        completed_ids = list(roadmap.get("completed_item_ids", []))
        items = list(roadmap.get("items", []))

        item_found = False
        new_status = False

        for item in items:
            if item.get("id") == item_id:
                item_found = True
                curr_status = item.get("completion_status") == "completed"
                if is_completed is None:
                    new_status = not curr_status
                else:
                    new_status = is_completed

                item["completion_status"] = "completed" if new_status else "upcoming"

                if new_status and item_id not in completed_ids:
                    completed_ids.append(item_id)
                elif not new_status and item_id in completed_ids:
                    completed_ids.remove(item_id)
                break

        if not item_found:
            return roadmap

        # Recalculate progress metrics
        total_items = len(items)
        completed_count = len(completed_ids)
        overall_progress = round((completed_count / max(1, total_items)) * 100, 1)

        # Update next recommended action
        next_action = None
        current_focus = "General Mastery"
        for item in items:
            if item.get("completion_status") != "completed":
                # Check prerequisites
                prereqs = item.get("prerequisites", [])
                prereqs_met = all(p in completed_ids for p in prereqs)
                if prereqs_met and not next_action:
                    next_action = item
                    current_focus = f"{item.get('category', 'Practice')} - {item.get('title', '')}"
                    break

        now = datetime.utcnow().isoformat()
        updates = {
            "completed_item_ids": completed_ids,
            "items": items,
            "overall_progress": overall_progress,
            "current_focus": current_focus,
            "next_recommended_action": next_action,
            "updated_at": now
        }

        await self.col.update_one({"user_id": str(user_id)}, {"$set": updates})
        return await self.get_by_user_id(user_id)

adaptive_roadmap_repository = AdaptiveRoadmapRepository()
