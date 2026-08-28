from datetime import datetime
from typing import Dict, Any, List, Optional
from app.database.mongodb import db_manager

class SpeechRepository:
    def __init__(self):
        pass

    def _col(self):
        return db_manager.get_collection("speech_analyses")

    async def create_analysis(self, user_id: str, analysis_doc: Dict[str, Any]) -> Dict[str, Any]:
        col = self._col()
        doc = dict(analysis_doc)
        doc["user_id"] = str(user_id)
        if "created_at" not in doc:
            doc["created_at"] = datetime.utcnow().isoformat()
        
        result = await col.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        doc["id"] = doc["_id"]
        return doc

    async def get_user_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        col = self._col()
        cursor = col.find({"user_id": str(user_id)}).sort("created_at", -1).limit(limit)
        items = await cursor.to_list(limit)
        for item in items:
            item["_id"] = str(item["_id"])
            if "id" not in item:
                item["id"] = item["_id"]
        return items

    async def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        col = self._col()
        items = await col.find({"user_id": str(user_id)}).sort("created_at", 1).to_list(50)
        
        if not items:
            return {
                "attempts_count": 0,
                "score_trend": [],
                "wpm_trend": [],
                "filler_ratio_trend": [],
                "latest_score": None
            }

        score_trend = []
        wpm_trend = []
        filler_trend = []

        for idx, item in enumerate(items):
            metrics = item.get("metrics", {})
            overall = item.get("overall_delivery_score", item.get("score", 70))
            wpm = metrics.get("words_per_minute", 135)
            filler_pct = metrics.get("filler_ratio_percentage", 3.0)
            
            score_trend.append({
                "attempt": f"Attempt {idx + 1}",
                "date": item.get("created_at", "")[:10],
                "score": overall
            })
            wpm_trend.append({
                "attempt": f"Attempt {idx + 1}",
                "wpm": wpm
            })
            filler_trend.append({
                "attempt": f"Attempt {idx + 1}",
                "filler_percentage": filler_pct
            })

        return {
            "attempts_count": len(items),
            "score_trend": score_trend,
            "wpm_trend": wpm_trend,
            "filler_ratio_trend": filler_trend,
            "latest_score": items[-1].get("overall_delivery_score", 75)
        }

speech_repository = SpeechRepository()
