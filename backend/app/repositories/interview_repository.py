from datetime import datetime
from typing import Optional, Dict, Any, List
from bson import ObjectId
from app.database.mongodb import db_manager

class InterviewRepository:
    def __init__(self):
        self.old_collection_name = "interview_results"
        self.sessions_collection_name = "mock_interview_sessions"

    @property
    def col(self):
        return db_manager.get_collection(self.old_collection_name)

    @property
    def sessions_col(self):
        return db_manager.get_collection(self.sessions_collection_name)

    async def create_session(self, user_id: str, session_data: Dict[str, Any]) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = dict(session_data)
        doc["user_id"] = str(user_id)
        doc["started_at"] = now
        doc["status"] = "active" # active, paused, completed
        doc["questions"] = doc.get("questions", [])
        doc["answers"] = doc.get("answers", [])
        doc["topics_covered"] = doc.get("topics_covered", [])
        doc["created_at"] = now
        doc["updated_at"] = now

        res = await self.sessions_col.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        doc["session_id"] = str(res.inserted_id)
        return doc

    async def save_session(self, user_id: str, session_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        return await self.create_session(user_id, session_data)

    async def get_session(self, session_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        # Enforce strict user isolation: search by session_id AND user_id
        try:
            doc = await self.sessions_col.find_one({"_id": ObjectId(session_id), "user_id": str(user_id)})
        except Exception:
            doc = await self.sessions_col.find_one({"session_id": str(session_id), "user_id": str(user_id)})

        if doc:
            doc["_id"] = str(doc.get("_id", ""))
            doc["session_id"] = str(doc.get("_id", ""))
        return doc

    async def update_session(self, session_id: str, user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        updates["updated_at"] = datetime.utcnow().isoformat()
        try:
            filter_dict = {"_id": ObjectId(session_id), "user_id": str(user_id)}
        except Exception:
            filter_dict = {"session_id": str(session_id), "user_id": str(user_id)}

        await self.sessions_col.update_one(filter_dict, {"$set": updates})
        return await self.get_session(session_id, user_id)

    async def add_question_and_answer(
        self,
        session_id: str,
        user_id: str,
        question_doc: Dict[str, Any],
        answer_doc: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        try:
            filter_dict = {"_id": ObjectId(session_id), "user_id": str(user_id)}
        except Exception:
            filter_dict = {"session_id": str(session_id), "user_id": str(user_id)}

        await self.sessions_col.update_one(
            filter_dict,
            {
                "$push": {
                    "questions": question_doc,
                    "answers": answer_doc
                },
                "$addToSet": {"topics_covered": question_doc.get("topic", "General")},
                "$set": {"updated_at": datetime.utcnow().isoformat()}
            }
        )
        return await self.get_session(session_id, user_id)

    async def list_user_sessions(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        cursor = self.sessions_col.find({"user_id": str(user_id)}).sort("created_at", -1)
        docs = await cursor.to_list(limit)
        for d in docs:
            d["_id"] = str(d.get("_id", ""))
            d["session_id"] = str(d.get("_id", ""))
        return docs

    async def save_session_evaluation(self, user_id: str, role: str, question: str, user_answer: str, evaluation: Dict[str, Any], session_type: str = "technical") -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = {
            "user_id": str(user_id),
            "role": role,
            "question": question,
            "user_answer": user_answer,
            "session_type": session_type,
            "score": evaluation.get("question_score", evaluation.get("score", 85)),
            "created_at": now
        }
        res = await self.col.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        doc["id"] = str(res.inserted_id)
        return doc

    async def get_user_interviews(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.list_user_sessions(user_id, limit)

    async def get_user_sessions(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        return await self.list_user_sessions(user_id, limit)

interview_repository = InterviewRepository()
