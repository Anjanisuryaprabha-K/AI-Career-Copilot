"""
Content repositories for cover letters, LinkedIn analyses, portfolio data, and company insights.

These replace the direct db_manager.get_collection() calls that were scattered across
cover_letter/router.py, linkedin/router.py, portfolio/router.py, and companies/router.py.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.mongodb import db_manager


class CoverLetterRepository:
    def __init__(self):
        self.collection_name = "cover_letters"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def save(self, user_id: str, target_role: str, company_name: str, cover_letter: Dict[str, Any]) -> None:
        """Persist a generated cover letter document, ignoring errors silently."""
        try:
            await self.col.insert_one({
                "user_id": user_id,
                "target_role": target_role,
                "company_name": company_name,
                "cover_letter": cover_letter,
                "created_at": datetime.utcnow().isoformat()
            })
        except Exception:
            pass

    async def get_user_letters(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.col.find({"user_id": user_id}).sort("created_at", -1).to_list(20)


class LinkedInRepository:
    def __init__(self):
        self.collection_name = "linkedin_analyses"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def save(self, user_id: str, target_role: str, skills: List[str], optimization: Dict[str, Any]) -> None:
        """Persist a LinkedIn optimization result, ignoring errors silently."""
        try:
            await self.col.insert_one({
                "user_id": user_id,
                "target_role": target_role,
                "skills": skills,
                "optimization": optimization,
                "created_at": datetime.utcnow().isoformat()
            })
        except Exception:
            pass

    async def get_user_analyses(self, user_id: str) -> List[Dict[str, Any]]:
        return await self.col.find({"user_id": user_id}).sort("created_at", -1).to_list(10)


class PortfolioRepository:
    def __init__(self):
        self.collection_name = "portfolio_data"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def upsert(self, user_id: str, target_role: str, portfolio: Dict[str, Any]) -> None:
        """Upsert portfolio data for a user, ignoring errors silently."""
        try:
            await self.col.update_one(
                {"user_id": user_id},
                {"$set": {
                    "user_id": user_id,
                    "target_role": target_role,
                    "portfolio": portfolio,
                    "updated_at": datetime.utcnow().isoformat()
                }},
                upsert=True
            )
        except Exception:
            pass

    async def get(self, user_id: str) -> Optional[Dict[str, Any]]:
        return await self.col.find_one({"user_id": user_id})


class CompanyInsightsRepository:
    def __init__(self):
        self.collection_name = "company_insights"

    @property
    def col(self):
        return db_manager.get_collection(self.collection_name)

    async def upsert_insights(self, company_id: str, insights: Dict[str, Any]) -> None:
        """Cache company insight data, ignoring errors silently."""
        try:
            await self.col.update_one(
                {"company_name": company_id.lower()},
                {"$set": {
                    "company_name": company_id.lower(),
                    "insights": insights,
                    "updated_at": datetime.utcnow().isoformat()
                }},
                upsert=True
            )
        except Exception:
            pass

    async def get_insights(self, company_id: str) -> Optional[Dict[str, Any]]:
        return await self.col.find_one({"company_name": company_id.lower()})


cover_letter_repository = CoverLetterRepository()
linkedin_repository = LinkedInRepository()
portfolio_repository = PortfolioRepository()
company_insights_repository = CompanyInsightsRepository()
