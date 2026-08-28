from datetime import datetime
from typing import Dict, Any
from app.database.mongodb import db_manager
from app.services.job_readiness_service import JobReadinessService

class AnalyticsRepository:
    def __init__(self):
        pass

    async def compute_user_analytics(self, user_id: str) -> Dict[str, Any]:
        apps_col = db_manager.get_collection("applications")
        scans_col = db_manager.get_collection("resume_analyses")
        interviews_col = db_manager.get_collection("interview_results")
        coding_col = db_manager.get_collection("coding_attempts")
        jobs_col = db_manager.get_collection("job_matches")
        
        apps = await apps_col.find({"user_id": str(user_id)}).to_list(100)
        scans = await scans_col.find({"user_id": str(user_id)}).to_list(10)
        interviews = await interviews_col.find({"user_id": str(user_id)}).to_list(50)
        coding = await coding_col.find({"user_id": str(user_id)}).to_list(50)
        saved_jobs = await jobs_col.find({"user_id": str(user_id), "saved": True}).to_list(50)

        # Call central readiness intelligence service
        readiness_data = await JobReadinessService.compute_user_readiness(user_id)
        breakdown = readiness_data.get("weighting_breakdown", {})

        total_apps = len(apps)
        interviewing_count = sum(1 for a in apps if a.get("status") in ["Interview", "Interviewing", "Technical Round 1", "Technical Round 2"])
        offers_count = sum(1 for a in apps if a.get("status") in ["Offer", "Offer Received"])
        coding_problems_solved = len(coding)
        interviews_completed = len(interviews)

        return {
            "user_id": str(user_id),
            "readiness_score": readiness_data["overall_readiness_score"],
            "tier": readiness_data["tier"],
            "resume_score": breakdown.get("resume_score", {}).get("score", 0),
            "skills_score": breakdown.get("skills_score", {}).get("score", 0),
            "coding_score": breakdown.get("coding_score", {}).get("score", 0),
            "interview_score": breakdown.get("interview_score", {}).get("score", 0),
            "profile_score": breakdown.get("profile_score", {}).get("score", 0),
            "application_score": breakdown.get("application_score", {}).get("score", 0),
            "total_applications": total_apps,
            "interviewing_count": interviewing_count,
            "offers_count": offers_count,
            "interviews_completed": interviews_completed,
            "coding_problems_solved": coding_problems_solved,
            "saved_jobs_count": len(saved_jobs),
            "strengths": readiness_data.get("strengths", []),
            "weaknesses": readiness_data.get("weaknesses", []),
            "recommended_actions": readiness_data.get("recommended_actions", []),
            "trend_history": readiness_data.get("trend_history", [])
        }

analytics_repository = AnalyticsRepository()
