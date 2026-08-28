from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid
from app.database.mongodb import db_manager

class ChatRepository:
    def __init__(self):
        self.collection_name = "chat_history"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def get_user_conversations(self, user_id: str) -> List[Dict[str, Any]]:
        cursor = self.col.find({"user_id": str(user_id)}).sort("updated_at", -1)
        return await cursor.to_list(50)

    async def get_conversation(self, user_id: str, conversation_id: str) -> Optional[Dict[str, Any]]:
        return await self.col.find_one({"user_id": str(user_id), "conversation_id": str(conversation_id)})

    async def save_message(self, user_id: str, conversation_id: str, user_message: str, ai_response: str, sources: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        conv = await self.get_conversation(user_id, conversation_id)
        msg_user = {"role": "user", "content": user_message, "timestamp": now}
        msg_ai = {"role": "assistant", "content": ai_response, "sources": sources or [], "timestamp": now}
        
        if not conv:
            title = user_message[:35] + "..." if len(user_message) > 35 else user_message
            doc = {
                "user_id": str(user_id),
                "conversation_id": conversation_id or str(uuid.uuid4()),
                "title": title,
                "messages": [msg_user, msg_ai],
                "created_at": now,
                "updated_at": now
            }
            await self.col.insert_one(doc)
            return doc
        else:
            await self.col.update_one(
                {"user_id": str(user_id), "conversation_id": conversation_id},
                {
                    "$push": {"messages": msg_user},
                    "$set": {"updated_at": now}
                }
            )
            await self.col.update_one(
                {"user_id": str(user_id), "conversation_id": conversation_id},
                {
                    "$push": {"messages": msg_ai},
                    "$set": {"updated_at": now}
                }
            )
            return await self.get_conversation(user_id, conversation_id)

    async def delete_conversation(self, user_id: str, conversation_id: str) -> bool:
        return await self.col.delete_one({"user_id": str(user_id), "conversation_id": conversation_id})

chat_repository = ChatRepository()
