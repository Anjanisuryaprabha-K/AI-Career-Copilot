from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager

class ResumeRepository:
    def __init__(self):
        self.scans_col_name = "resume_analyses"
        self.resumes_col_name = "resumes"

    @property
    def scans_col(self):
        return db_manager.get_collection(self.scans_col_name)

    @property
    def resumes_col(self):
        return db_manager.get_collection(self.resumes_col_name)

    async def save_scan(self, user_id: str, user_email: str, target_role: str, scan_data: Dict[str, Any], resume_preview: str = "") -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = {
            "user_id": str(user_id),
            "user_email": user_email.strip().lower(),
            "target_role": target_role,
            "overall_score": scan_data.get("overall_score", 0),
            "breakdown": scan_data.get("breakdown", {}),
            "matched_keywords": scan_data.get("matched_keywords", []),
            "missing_keywords": scan_data.get("missing_keywords", []),
            "recommendations": scan_data.get("critical_fixes", []),
            "structured_extraction": scan_data.get("structured_extraction", {}),
            "section_scores": scan_data.get("section_scores", {}),
            "weak_sections": scan_data.get("weak_sections", []),
            "strengths": scan_data.get("strengths", []),
            "jd_match_analysis": scan_data.get("jd_match_analysis", {}),
            "scan_data": scan_data,
            "resume_preview": resume_preview[:300] if resume_preview else "",
            "created_at": now,
            "updated_at": now
        }
        res = await self.scans_col.insert_one(doc)
        if hasattr(res, "inserted_id"):
            doc["_id"] = str(res.inserted_id)
            doc["id"] = str(res.inserted_id)
        return doc

    async def save_analysis(self, scan_data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        data = dict(scan_data) if isinstance(scan_data, dict) else {}
        data.update(kwargs)
        user_id = str(data.get("user_id", "default_user"))
        user_email = str(data.get("user_email", "user@example.com"))
        target_role = str(data.get("target_role", "Software Engineer"))
        if "overall_score" not in data and "ats_score" in data:
            data["overall_score"] = data["ats_score"]
        return await self.save_scan(user_id, user_email, target_role, data)

    async def save_resume_analysis(self, scan_data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        return await self.save_analysis(scan_data, **kwargs)

    async def get_user_scans(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        cursor = self.scans_col.find({"user_id": str(user_id)}).sort("created_at", -1)
        return await cursor.to_list(limit)

    async def get_latest_user_scan(self, user_id: str) -> Optional[Dict[str, Any]]:
        scans = await self.get_user_scans(user_id, limit=1)
        return scans[0] if scans else None

    async def get_latest_resume(self, user_id: str) -> Optional[Dict[str, Any]]:
        return await self.get_latest_user_scan(user_id)

    async def save_resume_file(self, user_id: str, filename: str, content_type: str, parsed_text: str, ats_score: int) -> Dict[str, Any]:
        now = datetime.utcnow().isoformat()
        doc = {
            "user_id": str(user_id),
            "filename": filename,
            "content_type": content_type,
            "parsed_text": parsed_text,
            "ats_score": ats_score,
            "created_at": now,
            "updated_at": now
        }
        res = await self.resumes_col.insert_one(doc)
        if hasattr(res, "inserted_id"):
            doc["_id"] = str(res.inserted_id)
            doc["id"] = str(res.inserted_id)
        return doc

    async def get_user_resumes(self, user_id: str) -> List[Dict[str, Any]]:
        cursor = self.resumes_col.find({"user_id": str(user_id)}).sort("created_at", -1)
        return await cursor.to_list(20)

resume_repository = ResumeRepository()
