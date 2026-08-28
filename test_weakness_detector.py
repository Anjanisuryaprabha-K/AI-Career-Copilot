import asyncio
import unittest
from datetime import datetime
from app.services.weakness_detector_service import WeaknessDetectorService
from app.repositories.weakness_repository import weakness_repository
from app.repositories.coding_repository import CodingRepository
from app.repositories.resume_repository import resume_repository
from app.repositories.interview_repository import InterviewRepository

coding_repo = CodingRepository()
interview_repo = InterviewRepository()

class TestWeaknessDetector(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.user_new = f"test_usr_new_{int(datetime.utcnow().timestamp())}"
        self.user_active = f"test_usr_act_{int(datetime.utcnow().timestamp())}"
        self.user_isolated = f"test_usr_iso_{int(datetime.utcnow().timestamp())}"

    def test_01_insufficient_data_handling(self):
        async def run():
            # User with 0 activity across modules
            analysis = await WeaknessDetectorService.analyze_user_weaknesses(self.user_new)
            self.assertEqual(analysis["user_id"], self.user_new)
            self.assertFalse(analysis["has_sufficient_data"])
            self.assertIn("Not enough data yet", analysis["message"])
            self.assertEqual(len(analysis["top_weaknesses"]), 0)
            self.assertEqual(len(analysis["top_strengths"]), 0)
            self.assertIsNone(analysis["highest_impact_improvement"])

        self.loop.run_until_complete(run())

    def test_02_weakness_calculation_and_ranking(self):
        async def run():
            # 1. Record resume scan for active user
            await resume_repository.save_analysis({
                "user_id": self.user_active,
                "overall_score": 58,
                "section_scores": {"Summary": 60, "Experience": 50, "Projects": 65},
                "missing_keywords": ["Docker", "Kubernetes", "Microservices"]
            })

            # 2. Record coding attempts
            await coding_repo.record_attempt(
                user_id=self.user_active,
                problem_id="p1_two_sum",
                language="python",
                code="def solution(): return False",
                execution_result={"status": "Wrong Answer", "passed_count": 1, "total_count": 5}
            )

            # 3. Record mock interview session
            await interview_repo.save_session(self.user_active, {
                "session_id": f"sess_{self.user_active}",
                "user_id": self.user_active,
                "overall_score": 72,
                "feedback": "Good communication, review system architecture."
            })

            # Run analysis
            analysis = await WeaknessDetectorService.analyze_user_weaknesses(self.user_active)
            self.assertTrue(analysis["has_sufficient_data"])
            self.assertGreater(len(analysis["top_weaknesses"]), 0)
            self.assertGreater(len(analysis["top_strengths"]), 0)

            # Verify weaknesses are ranked ascending by score
            weaknesses = analysis["top_weaknesses"]
            for i in range(len(weaknesses) - 1):
                self.assertLessEqual(weaknesses[i]["current_score"], weaknesses[i + 1]["current_score"])

            # Verify strengths are ranked descending by score
            strengths = analysis["top_strengths"]
            for i in range(len(strengths) - 1):
                self.assertGreaterEqual(strengths[i]["current_score"], strengths[i + 1]["current_score"])

        self.loop.run_until_complete(run())

    def test_03_highest_impact_improvement_generation(self):
        async def run():
            # Record low ATS score
            await resume_repository.save_analysis({
                "user_id": self.user_active,
                "overall_score": 42,
                "missing_keywords": ["CI/CD", "AWS"]
            })

            analysis = await WeaknessDetectorService.analyze_user_weaknesses(self.user_active)
            highest_impact = analysis["highest_impact_improvement"]

            self.assertIsNotNone(highest_impact)
            self.assertIn("weakness_title", highest_impact)
            self.assertIn("impact_statement", highest_impact)
            self.assertIn("recommended_action", highest_impact)
            self.assertIn("target_link", highest_impact)

        self.loop.run_until_complete(run())

    def test_04_user_data_isolation(self):
        async def run():
            # Activity for user_active
            await resume_repository.save_analysis({
                "user_id": self.user_active,
                "overall_score": 85
            })

            analysis_act = await WeaknessDetectorService.analyze_user_weaknesses(self.user_active)
            analysis_iso = await WeaknessDetectorService.analyze_user_weaknesses(self.user_isolated)

            self.assertTrue(analysis_act["has_sufficient_data"])
            self.assertFalse(analysis_iso["has_sufficient_data"])

            # Verify isolated user has zero weaknesses from user_active
            db_iso_doc = await weakness_repository.get_latest_by_user_id(self.user_isolated)
            self.assertEqual(db_iso_doc["user_id"], self.user_isolated)
            self.assertFalse(db_iso_doc["has_sufficient_data"])

        self.loop.run_until_complete(run())

if __name__ == "__main__":
    unittest.main()
