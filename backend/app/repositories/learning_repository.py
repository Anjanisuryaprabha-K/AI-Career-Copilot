from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager

class LearningRepository:
    def __init__(self):
        self.progress_col_name = "learning_progress"
        self.video_progress_col_name = "user_video_progress"
        self.skill_gap_col_name = "skill_gap_results"

        self.bookmarks_col_name = "user_resource_bookmarks"
        self.resource_progress_col_name = "user_resource_progress"
        self.admin_resources_col_name = "admin_learning_resources"

        # Catalog Collections
        self.topics_col_name = "technical_topics"
        self.resources_col_name = "learning_resources"

    @property
    def progress_col(self):
        return db_manager.get_collection(self.progress_col_name)

    @property
    def video_col(self):
        return db_manager.get_collection(self.video_progress_col_name)

    @property
    def gap_col(self):
        return db_manager.get_collection(self.skill_gap_col_name)

    @property
    def bookmarks_col(self):
        return db_manager.get_collection(self.bookmarks_col_name)

    @property
    def resource_progress_col(self):
        return db_manager.get_collection(self.resource_progress_col_name)

    @property
    def admin_resources_col(self):
        return db_manager.get_collection(self.admin_resources_col_name)

    @property
    def topics_col(self):
        return db_manager.get_collection(self.topics_col_name)

    @property
    def resources_col(self):
        return db_manager.get_collection(self.resources_col_name)

    async def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        doc = await self.progress_col.find_one({"user_id": str(user_id)})
        if not doc:
            doc = {
                "user_id": str(user_id),
                "completed_milestones": ["m1", "m2"],
                "active_roadmap": "Full Stack Placement Ready 2026",
                "progress_percentage": 65,
                "updated_at": datetime.utcnow().isoformat()
            }
            await self.progress_col.insert_one(doc)
        return doc

    async def update_user_progress(self, user_id: str, completed_milestones: List[str], progress_pct: int) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        await self.progress_col.update_one(
            {"user_id": str(user_id)},
            {"$set": {"completed_milestones": completed_milestones, "progress_percentage": progress_pct, "updated_at": now}},
            upsert=True
        )
        return await self.get_user_progress(user_id)

    async def get_user_video_progress(self, user_id: str, track_id: str) -> List[str]:
        doc = await self.video_col.find_one({"user_id": str(user_id), "track_id": str(track_id)})
        if not doc:
            return []
        return doc.get("completed_video_ids", [])

    async def toggle_video_progress(self, user_id: str, track_id: str, video_id: str, is_completed: bool) -> List[str]:
        doc = await self.video_col.find_one({"user_id": str(user_id), "track_id": str(track_id)})
        completed = list(doc.get("completed_video_ids", [])) if doc else []

        if is_completed:
            if video_id not in completed:
                completed.append(video_id)
        else:
            if video_id in completed:
                completed.remove(video_id)

        now = datetime.utcnow().isoformat()
        await self.video_col.update_one(
            {"user_id": str(user_id), "track_id": str(track_id)},
            {"$set": {"completed_video_ids": completed, "updated_at": now}},
            upsert=True
        )
        return completed

    async def save_skill_gap_analysis(self, user_id: str, target_role: str, gap_result: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = {
            "user_id": str(user_id),
            "target_role": target_role,
            "readiness_score": gap_result.get("readiness_score", 75),
            "matched_skills": gap_result.get("matched_skills", []),
            "missing_skills": gap_result.get("missing_skills", []),
            "created_at": now
        }
        await self.gap_col.insert_one(doc)
        return doc

    # ==========================================
    # CATALOG & SEEDING METHODS (MONGODB)
    # ==========================================

    async def seed_catalog_if_needed(self, catalog: List[Dict[str, Any]]) -> bool:
        """
        Idempotent seeding of topics and resources into MongoDB if technical_topics is empty.
        """
        count = await self.topics_col.count_documents({})
        if count > 0:
            return False  # Already seeded

        now = datetime.utcnow().isoformat()
        for topic in catalog:
            t_doc = dict(topic)
            resources = t_doc.pop("resources", [])
            t_doc["updated_at"] = now
            if "_id" in t_doc:
                t_doc.pop("_id")

            await self.topics_col.update_one(
                {"id": t_doc["id"]},
                {"$set": t_doc},
                upsert=True
            )

            for res in resources:
                r_doc = dict(res)
                r_doc["updated_at"] = now
                if "_id" in r_doc:
                    r_doc.pop("_id")

                await self.resources_col.update_one(
                    {"id": r_doc["id"]},
                    {"$set": r_doc},
                    upsert=True
                )

        return True

    async def get_all_catalog_topics(self) -> List[Dict[str, Any]]:
        cursor = self.topics_col.find({})
        topics = await cursor.to_list(length=200)
        for t in topics:
            if "_id" in t:
                t["_id"] = str(t["_id"])
        return topics

    async def get_topic_by_id_or_slug(self, topic_id: str) -> Optional[Dict[str, Any]]:
        t_doc = await self.topics_col.find_one({"$or": [{"id": topic_id}, {"slug": topic_id}]})
        if not t_doc:
            return None
        if "_id" in t_doc:
            t_doc["_id"] = str(t_doc["_id"])

        # Fetch resources for this topic
        cursor = self.resources_col.find({"$or": [{"topic_id": t_doc["id"]}, {"topic": t_doc["title"]}]}).sort("order", 1)
        resources = await cursor.to_list(length=300)
        for r in resources:
            if "_id" in r:
                r["_id"] = str(r["_id"])
        t_doc["resources"] = resources
        return t_doc

    async def get_resources_by_topic(self, topic_id: str) -> List[Dict[str, Any]]:
        cursor = self.resources_col.find({"$or": [{"topic_id": topic_id}, {"topic": topic_id}]}).sort("order", 1)
        resources = await cursor.to_list(length=300)
        for r in resources:
            if "_id" in r:
                r["_id"] = str(r["_id"])
        return resources

    # ==========================================
    # YOUTUBE RESOURCE BOOKMARKS & PROGRESS METHODS
    # ==========================================

    async def get_user_bookmarks(self, user_id: str) -> List[Dict[str, Any]]:
        cursor = self.bookmarks_col.find({"user_id": str(user_id)})
        bookmarks = await cursor.to_list(length=200)
        for b in bookmarks:
            if "_id" in b:
                b["_id"] = str(b["_id"])
        return bookmarks

    async def add_bookmark(self, user_id: str, resource: Dict[str, Any]) -> Dict[str, Any]:
        resource_id = resource.get("id") or resource.get("resource_id")
        now = datetime.utcnow().isoformat()
        doc = {
            "user_id": str(user_id),
            "resource_id": str(resource_id),
            "topic": resource.get("topic", "General"),
            "resource": resource,
            "bookmarked_at": now
        }
        await self.bookmarks_col.update_one(
            {"user_id": str(user_id), "resource_id": str(resource_id)},
            {"$set": doc},
            upsert=True
        )
        return doc

    async def remove_bookmark(self, user_id: str, resource_id: str) -> bool:
        res = await self.bookmarks_col.delete_one({"user_id": str(user_id), "resource_id": str(resource_id)})
        return res.deleted_count > 0

    async def get_user_resource_progress(self, user_id: str) -> Dict[str, Dict[str, Any]]:
        cursor = self.resource_progress_col.find({"user_id": str(user_id)})
        items = await cursor.to_list(length=500)
        res_map = {}
        for item in items:
            rid = item.get("resource_id")
            if rid:
                res_map[rid] = {
                    "status": item.get("status", "not_started"),
                    "updated_at": item.get("updated_at")
                }
        return res_map

    async def set_resource_progress(self, user_id: str, resource_id: str, status: str, topic: Optional[str] = None) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = {
            "user_id": str(user_id),
            "resource_id": str(resource_id),
            "topic": topic or "General",
            "status": status,
            "updated_at": now
        }
        await self.resource_progress_col.update_one(
            {"user_id": str(user_id), "resource_id": str(resource_id)},
            {"$set": doc},
            upsert=True
        )
        return doc

    # ==========================================
    # ADMIN LEARNING RESOURCE MANAGEMENT
    # ==========================================

    async def save_admin_resource(self, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = dict(resource_data)
        doc["updated_at"] = now
        if "created_at" not in doc:
            doc["created_at"] = now
        
        resource_id = doc.get("id") or f"admin_res_{int(datetime.utcnow().timestamp())}"
        doc["id"] = resource_id

        await self.admin_resources_col.update_one(
            {"id": resource_id},
            {"$set": doc},
            upsert=True
        )
        return doc

    async def delete_admin_resource(self, resource_id: str) -> bool:
        res = await self.admin_resources_col.delete_one({"id": resource_id})
        return res.deleted_count > 0

    async def list_admin_resources(self) -> List[Dict[str, Any]]:
        cursor = self.admin_resources_col.find({})
        resources = await cursor.to_list(length=200)
        for r in resources:
            if "_id" in r:
                r["_id"] = str(r["_id"])
        return resources

learning_repository = LearningRepository()
