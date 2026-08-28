import os
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, status
from app.config import settings
from app.database.bson_utils import sanitize_doc, sanitize_docs

class InMemoryCursor:
    def __init__(self, items: List[Dict[str, Any]]):
        self._items = [dict(it) for it in items]

    def sort(self, key_or_list, direction: int = -1):
        if isinstance(key_or_list, list):
            for key, direct in reversed(key_or_list):
                reverse = (direct == -1)
                self._items.sort(key=lambda x: str(x.get(key, "")), reverse=reverse)
        else:
            reverse = (direction == -1)
            self._items.sort(key=lambda x: str(x.get(key_or_list, "")), reverse=reverse)
        return self

    def skip(self, count: int):
        self._items = self._items[count:]
        return self

    def limit(self, count: int):
        self._items = self._items[:count]
        return self

    async def to_list(self, length: Optional[int] = 100) -> List[Dict[str, Any]]:
        if length is not None:
            return self._items[:length]
        return self._items

    def __aiter__(self):
        self._iter = iter(self._items)
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration


class InMemoryCollection:
    def __init__(self, name: str):
        self.name = name
        self._docs: Dict[str, Dict[str, Any]] = {}
        self._counter = 1
        self._indexes = []

    def _matches_filter(self, doc: Dict[str, Any], filter_dict: Dict[str, Any]) -> bool:
        for k, v in filter_dict.items():
            if k == "_id":
                if str(doc.get("_id", "")) != str(v) and str(doc.get("id", "")) != str(v):
                    return False
            elif k == "id":
                if str(doc.get("id", "")) != str(v) and str(doc.get("_id", "")) != str(v):
                    return False
            elif isinstance(v, dict):
                doc_val = doc.get(k)
                if "$in" in v and doc_val not in v["$in"]:
                    return False
                if "$ne" in v and doc_val == v["$ne"]:
                    return False
            else:
                if doc.get(k) != v:
                    return False
        return True

    async def find_one(self, filter_dict: Dict[str, Any], sort: Optional[Any] = None, **kwargs) -> Optional[Dict[str, Any]]:
        matches = [d for d in self._docs.values() if self._matches_filter(d, filter_dict)]
        if not matches:
            return None
        if sort and isinstance(sort, list) and len(sort) > 0:
            key, order = sort[0]
            reverse = True if order in (-1, "descending", "desc") else False
            matches.sort(key=lambda x: str(x.get(key, "")), reverse=reverse)
        return dict(matches[0])

    def find(self, filter_dict: Optional[Dict[str, Any]] = None):
        filter_dict = filter_dict or {}
        matches = [d for d in self._docs.values() if self._matches_filter(d, filter_dict)]
        return InMemoryCursor(matches)

    async def insert_one(self, doc: Dict[str, Any]) -> Any:
        doc_copy = dict(doc)
        if "_id" not in doc_copy:
            doc_copy["_id"] = f"{self.name}_{self._counter}"
            self._counter += 1
        if "id" not in doc_copy:
            doc_copy["id"] = str(doc_copy["_id"])
        
        doc_id = str(doc_copy["_id"])
        self._docs[doc_id] = doc_copy
        
        class InsertResult:
            inserted_id = doc_copy["_id"]
        return InsertResult()

    async def update_one(self, filter_dict: Dict[str, Any], update_dict: Dict[str, Any], upsert: bool = False) -> Any:
        existing = await self.find_one(filter_dict)
        if existing:
            doc_id = str(existing["_id"])
            target = self._docs[doc_id]
            if "$set" in update_dict:
                target.update(update_dict["$set"])
            if "$unset" in update_dict:
                for k in update_dict["$unset"]:
                    target.pop(k, None)
            if "$push" in update_dict:
                for k, v in update_dict["$push"].items():
                    if k not in target or not isinstance(target[k], list):
                        target[k] = []
                    target[k].append(v)
            if not any(k.startswith("$") for k in update_dict):
                target.update(update_dict)
            return True
        elif upsert:
            new_doc = dict(filter_dict)
            if "$set" in update_dict:
                new_doc.update(update_dict["$set"])
            await self.insert_one(new_doc)
            return True
        return False

    async def delete_one(self, filter_dict: Dict[str, Any]) -> bool:
        for k, d in list(self._docs.items()):
            if self._matches_filter(d, filter_dict):
                del self._docs[k]
                return True
        return False

    async def delete_many(self, filter_dict: Dict[str, Any]) -> int:
        count = 0
        for k, d in list(self._docs.items()):
            if self._matches_filter(d, filter_dict):
                del self._docs[k]
                count += 1
        return count

    async def count_documents(self, filter_dict: Dict[str, Any]) -> int:
        return sum(1 for d in self._docs.values() if self._matches_filter(d, filter_dict))

    async def create_index(self, keys, **kwargs):
        self._indexes.append((keys, kwargs))
        return "index_created"


class MongoCollectionWrapper:
    """Thin wrapper around a Motor collection that sanitizes BSON ObjectIds."""
    def __init__(self, collection):
        self._col = collection

    async def find_one(self, filter_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        doc = await self._col.find_one(filter_dict)
        return sanitize_doc(doc)

    def find(self, filter_dict: Optional[Dict[str, Any]] = None):
        return SanitizedCursor(self._col.find(filter_dict or {}))

    async def insert_one(self, doc: Dict[str, Any]):
        return await self._col.insert_one(doc)

    async def update_one(self, filter_dict, update_dict, upsert: bool = False):
        return await self._col.update_one(filter_dict, update_dict, upsert=upsert)

    async def delete_one(self, filter_dict: Dict[str, Any]):
        return await self._col.delete_one(filter_dict)

    async def delete_many(self, filter_dict: Dict[str, Any]):
        return await self._col.delete_many(filter_dict)

    async def count_documents(self, filter_dict: Dict[str, Any]) -> int:
        return await self._col.count_documents(filter_dict)

    async def create_index(self, keys, **kwargs):
        return await self._col.create_index(keys, **kwargs)


class SanitizedCursor:
    """Wraps a Motor cursor to sanitize documents on conversion."""
    def __init__(self, cursor):
        self._cursor = cursor

    def sort(self, key_or_list, direction=None):
        if direction is not None:
            self._cursor = self._cursor.sort(key_or_list, direction)
        else:
            self._cursor = self._cursor.sort(key_or_list)
        return self

    def skip(self, count: int):
        self._cursor = self._cursor.skip(count)
        return self

    def limit(self, count: int):
        self._cursor = self._cursor.limit(count)
        return self

    async def to_list(self, length: Optional[int] = 100) -> List[Dict[str, Any]]:
        docs = await self._cursor.to_list(length=length)
        return sanitize_docs(docs)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            doc = await self._cursor.__anext__()
            return sanitize_doc(doc)
        except StopAsyncIteration:
            raise


class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        self._in_memory_collections: Dict[str, InMemoryCollection] = {}
        self.is_connected = False

    async def connect(self):
        if settings.USE_IN_MEMORY_DB:
            self.is_connected = True
            print("[Database] Running in explicit Development In-Memory Mode (USE_IN_MEMORY_DB=true)")
            await self.init_indexes()
            return

        try:
            import motor.motor_asyncio
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                settings.MONGODB_URL, serverSelectionTimeoutMS=2000
            )
            # Verify real live MongoDB connection
            await self.client.admin.command("ping")
            self.db = self.client[settings.MONGODB_DATABASE]
            self.is_connected = True
            print(f"[MongoDB] Connected successfully to database '{settings.MONGODB_DATABASE}' at {settings.MONGODB_URL}")
            await self.init_indexes()
        except Exception as e:
            self.is_connected = False
            self.db = None
            print(f"[MongoDB Error] Could not connect to MongoDB at {settings.MONGODB_URL}: {e}")
            print("[MongoDB Warning] Database is unavailable. Requests requiring persistence will return HTTP 503 until MongoDB is online.")

    async def disconnect(self):
        if self.client:
            self.client.close()
            self.is_connected = False
            print("[MongoDB] Disconnected from database.")

    def get_collection(self, name: str):
        if self.is_connected and self.db is not None:
            # Wrap with sanitizer so ObjectIds never reach JSON encoder
            return MongoCollectionWrapper(self.db[name])
        
        # Fallback to in-memory collection for development & resilience
        if name not in self._in_memory_collections:
            self._in_memory_collections[name] = InMemoryCollection(name)
        return self._in_memory_collections[name]

    async def init_indexes(self):
        collections = [
            ("users", [("email", 1)], {"unique": True}),
            ("resumes", [("user_id", 1), ("created_at", -1)], {}),
            ("resume_analyses", [("user_id", 1), ("created_at", -1)], {}),
            ("job_searches", [("user_id", 1), ("created_at", -1)], {}),
            ("job_matches", [("user_id", 1), ("created_at", -1)], {}),
            ("applications", [("user_id", 1), ("created_at", -1)], {}),
            ("interviews", [("user_id", 1), ("created_at", -1)], {}),
            ("interview_results", [("user_id", 1), ("created_at", -1)], {}),
            ("coding_attempts", [("user_id", 1), ("problem_id", 1), ("created_at", -1)], {}),
            ("skill_gap_results", [("user_id", 1), ("created_at", -1)], {}),
            ("learning_progress", [("user_id", 1), ("created_at", -1)], {}),
            ("github_analyses", [("user_id", 1), ("created_at", -1)], {}),
            ("linkedin_analyses", [("user_id", 1), ("created_at", -1)], {}),
            ("cover_letters", [("user_id", 1), ("created_at", -1)], {}),
            ("portfolio_data", [("user_id", 1), ("created_at", -1)], {}),
            ("chat_history", [("user_id", 1), ("conversation_id", 1), ("created_at", -1)], {}),
            ("notifications", [("user_id", 1), ("read", 1), ("created_at", -1)], {}),
            ("analytics", [("user_id", 1), ("created_at", -1)], {}),
            ("company_insights", [("company_name", 1), ("created_at", -1)], {}),
            ("salary_predictions", [("user_id", 1), ("created_at", -1)], {}),
            ("search_cache", [("normalized_query", 1), ("search_type", 1)], {}),
            ("weakness_detector", [("user_id", 1), ("created_at", -1)], {}),
            ("skill_radar", [("user_id", 1), ("created_at", -1)], {}),
            ("study_plans", [("user_id", 1), ("created_at", -1)], {}),
            ("company_prep", [("user_id", 1), ("company_name", 1)], {}),
            ("gd_history", [("user_id", 1), ("created_at", -1)], {}),
            ("adaptive_roadmaps", [("user_id", 1), ("created_at", -1)], {}),
        ]
        for col_name, keys, kwargs in collections:
            try:
                col = self.get_collection(col_name)
                await col.create_index(keys, **kwargs)
            except Exception:
                pass

db_manager = DatabaseManager()
mongodb = db_manager
