from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager

class SearchCacheRepository:
    def __init__(self):
        self.collection_name = "search_cache"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    def normalize_query(self, query: str) -> str:
        return " ".join(query.strip().lower().split())

    async def get_cached_results(self, query: str, search_type: str = "all") -> Optional[Dict[str, Any]]:
        norm = self.normalize_query(query)
        cached = await self.col.find_one({"normalized_query": norm, "search_type": search_type})
        if cached:
            # Check expiration (e.g. 6 hours TTL)
            exp = cached.get("expires_at")
            if exp:
                try:
                    exp_dt = datetime.fromisoformat(exp)
                    if datetime.utcnow() > exp_dt:
                        await self.col.delete_one({"_id": cached["_id"]})
                        return None
                except Exception:
                    pass
            return cached
        return None

    async def set_cache(self, query: str, results: List[Dict[str, Any]], search_type: str = "all", ttl_hours: int = 6) -> Dict[str, Any]:
        norm = self.normalize_query(query)
        now = datetime.utcnow()
        doc = {
            "query": query,
            "normalized_query": norm,
            "search_type": search_type,
            "results": results,
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(hours=ttl_hours)).isoformat()
        }
        await self.col.update_one(
            {"normalized_query": norm, "search_type": search_type},
            {"$set": doc},
            upsert=True
        )
        return doc

search_cache_repository = SearchCacheRepository()
