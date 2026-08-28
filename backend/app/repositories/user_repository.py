from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager

class UserRepository:
    def __init__(self):
        self.collection_name = "users"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return await self.col.find_one({"email": email.strip().lower()})

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return await self.col.find_one({"_id": user_id}) or await self.col.find_one({"id": user_id})

    async def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        user_doc = dict(user_data)
        user_doc["email"] = user_doc["email"].strip().lower()
        now = datetime.utcnow().isoformat()
        if "created_at" not in user_doc:
            user_doc["created_at"] = now
        if "updated_at" not in user_doc:
            user_doc["updated_at"] = now
        if "settings" not in user_doc:
            user_doc["settings"] = {
                "theme": "dark",
                "notifications": True,
                "target_roles": ["Software Engineer", "Full Stack Developer"],
                "preferred_locations": ["Remote", "Bengaluru", "Hyderabad"],
                "remote_preference": True
            }
        res = await self.col.insert_one(user_doc)
        if hasattr(res, "inserted_id") and "_id" not in user_doc:
            user_doc["_id"] = str(res.inserted_id)
        user_doc["id"] = str(user_doc.get("_id", ""))
        return user_doc

    async def update(self, user_id_or_email: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        updates["updated_at"] = datetime.utcnow().isoformat()
        filter_dict = {"email": user_id_or_email.strip().lower()} if "@" in user_id_or_email else {"_id": user_id_or_email}
        await self.col.update_one(filter_dict, {"$set": updates})
        return await self.get_by_email(user_id_or_email) if "@" in user_id_or_email else await self.get_by_id(user_id_or_email)

    async def update_settings(self, user_id: str, settings_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.update(user_id, {"settings": settings_data})

    async def update_coding_profiles(self, user_id_or_email: str, profiles_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self.update(user_id_or_email, {"codingProfiles": profiles_data})

    async def list_all(self) -> List[Dict[str, Any]]:
        return await self.col.find().to_list(100)

user_repository = UserRepository()
