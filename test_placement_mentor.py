import asyncio
import unittest
from datetime import datetime
from app.services.placement_mentor_service import PlacementMentorService
from app.repositories.resume_repository import resume_repository
from app.repositories.coding_repository import coding_repository
from app.repositories.chat_repository import chat_repository

class TestPlacementMentor(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.user_a = f"test_usr_mentor_a_{int(datetime.utcnow().timestamp())}"
        self.user_b = f"test_usr_mentor_b_{int(datetime.utcnow().timestamp())}"

    def test_01_missing_data_handling(self):
        async def run():
            # User A has 0 resume scans or interviews recorded
            ctx = await PlacementMentorService.gather_user_mentor_context(self.user_a)
            self.assertFalse(ctx["has_resume_data"])
            self.assertFalse(ctx["has_interview_data"])

            res = await PlacementMentorService.generate_mentor_response(
                user_id=self.user_a,
                user_message="How can I improve my resume ATS score?"
            )
            self.assertEqual(res["status"], "success")
            self.assertIn("don't have enough data", res["reply"].lower())

        self.loop.run_until_complete(run())

    def test_02_personalized_answers_with_platform_data(self):
        async def run():
            # Seed resume scan for User B
            await resume_repository.save_resume_analysis(
                user_id=self.user_b,
                file_name="test_resume.pdf",
                ats_score=85,
                section_scores={"skills": 90, "projects": 80},
                missing_skills=["Docker", "Kubernetes"],
                target_role="Full Stack Developer"
            )

            # Seed coding progress for User B
            await coding_repository.record_attempt(
                user_id=self.user_b,
                problem_id="p1",
                submitted_code="print('hello')",
                status="Accepted",
                passed_testcases=5,
                total_testcases=5,
                execution_time_ms=120,
                memory_kb=1024,
                language="python"
            )

            ctx = await PlacementMentorService.gather_user_mentor_context(self.user_b)
            self.assertTrue(ctx["has_resume_data"])
            self.assertEqual(ctx["resume"]["ats_score"], 85)
            self.assertTrue(ctx["has_coding_data"])

            # Ask personalized question
            res = await PlacementMentorService.generate_mentor_response(
                user_id=self.user_b,
                user_message="Am I ready for a Software Engineer interview?"
            )
            self.assertEqual(res["status"], "success")
            self.assertIn("85", res["reply"])
            
            # Verify actionable recommendations returned with route links
            recs = res.get("actionable_recommendations", [])
            self.assertGreater(len(recs), 0)
            self.assertTrue(any("/coding-arena" in r["route"] or "/interview-simulator" in r["route"] for r in recs))

        self.loop.run_until_complete(run())

    def test_03_user_isolation(self):
        async def run():
            # User B has resume data; User A does not
            ctx_a = await PlacementMentorService.gather_user_mentor_context(self.user_a)
            ctx_b = await PlacementMentorService.gather_user_mentor_context(self.user_b)

            self.assertFalse(ctx_a["has_resume_data"])
            self.assertTrue(ctx_b["has_resume_data"])
            self.assertNotEqual(ctx_a["resume"].get("ats_score", 0), ctx_b["resume"].get("ats_score", 0))

        self.loop.run_until_complete(run())

    def test_04_ai_failure_fallback_graceful_handling(self):
        async def run():
            # Request with empty or offline Gemini handling
            res = await PlacementMentorService.generate_mentor_response(
                user_id=self.user_b,
                user_message="What should I study today?"
            )
            self.assertEqual(res["status"], "success")
            self.assertTrue(any(w in res["reply"].lower() for w in ["study", "practice", "plan"]))
            self.assertIn("coding arena", res["reply"].lower())

        self.loop.run_until_complete(run())

if __name__ == "__main__":
    unittest.main()
