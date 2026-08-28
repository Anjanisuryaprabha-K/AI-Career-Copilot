from typing import Optional, Dict, Any, List
from datetime import datetime
from app.database.mongodb import db_manager

class SkillRadarRepository:
    def __init__(self):
        self._in_memory_snapshots: Dict[str, List[Dict[str, Any]]] = {}

    def _get_collection(self):
        try:
            return db_manager.get_collection("user_skill_radar")
        except Exception:
            return None

    async def save_snapshot(self, user_id: str, snapshot_data: Dict[str, Any]) -> Dict[str, Any]:
        user_id_str = str(user_id)
        coll = self._get_collection()

        doc = {
            "user_id": user_id_str,
            "target_role": snapshot_data.get("target_role", "Software Engineer"),
            "evaluated_axes": snapshot_data.get("evaluated_axes", {}),
            "target_benchmarks": snapshot_data.get("target_benchmarks", {}),
            "highest_gap": snapshot_data.get("highest_gap", {}),
            "overall_average_score": snapshot_data.get("overall_average_score", 0),
            "created_at": datetime.utcnow().isoformat()
        }

        if coll is not None:
            await coll.insert_one(doc)
            doc["_id"] = str(doc.get("_id", ""))
        else:
            if user_id_str not in self._in_memory_snapshots:
                self._in_memory_snapshots[user_id_str] = []
            self._in_memory_snapshots[user_id_str].append(doc)

        return doc

    async def get_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        user_id_str = str(user_id)
        coll = self._get_collection()

        if coll is not None:
            cursor = coll.find({"user_id": user_id_str}).sort("created_at", -1).limit(limit)
            docs = await cursor.to_list(length=limit)
            for d in docs:
                d["_id"] = str(d["_id"])
            return docs

        snaps = self._in_memory_snapshots.get(user_id_str, [])
        return sorted(snaps, key=lambda x: x.get("created_at", ""), reverse=True)[:limit]

skill_radar_repository = SkillRadarRepository()
