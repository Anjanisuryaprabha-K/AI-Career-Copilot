import asyncio
import unittest
from datetime import datetime
from app.services.skill_radar_service import SkillRadarService
from app.repositories.resume_repository import resume_repository
from app.repositories.coding_repository import coding_repository

class TestSkillRadar(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.user_empty = f"test_usr_radar_empty_{int(datetime.utcnow().timestamp())}"
        self.user_active = f"test_usr_radar_active_{int(datetime.utcnow().timestamp())}"

    def test_01_not_enough_data_handling(self):
        async def run():
            # Empty user with no platform activity
            radar = await SkillRadarService.compute_skill_radar(self.user_empty, "Software Engineer")
            axes = radar["evaluated_axes"]
            
            # Must mark un-evaluated categories as "not_enough_data"
            self.assertEqual(axes["Interview"]["status"], "not_enough_data")
            self.assertIsNone(axes["Interview"]["score"])
            self.assertEqual(axes["Resume"]["status"], "not_enough_data")
            self.assertIsNone(axes["Resume"]["score"])

        self.loop.run_until_complete(run())

    def test_02_empirical_score_calculation_and_gap_analysis(self):
        async def run():
            # Seed resume & coding data for user_active
            await resume_repository.save_resume_analysis(
                user_id=self.user_active,
                file_name="resume.pdf",
                ats_score=88,
                section_scores={"projects": 85, "skills": 90},
                missing_skills=["Docker"],
                target_role="Software Engineer"
            )

            await coding_repository.record_attempt(
                user_id=self.user_active,
                problem_id="p_sql_1",
                submitted_code="SELECT * FROM users",
                status="Accepted",
                passed_testcases=5,
                total_testcases=5,
                execution_time_ms=100,
                memory_kb=512,
                language="sql"
            )

            radar = await SkillRadarService.compute_skill_radar(self.user_active, "Software Engineer")
            axes = radar["evaluated_axes"]

            self.assertEqual(axes["Resume"]["status"], "evaluated")
            self.assertEqual(axes["Resume"]["score"], 88)
            self.assertEqual(axes["SQL"]["status"], "evaluated")
            self.assertGreater(axes["SQL"]["score"], 0)

            # Check Highest Skill Gap card
            highest_gap = radar["highest_gap"]
            self.assertIn("axis", highest_gap)
            self.assertIn("recommended_action", highest_gap)
            self.assertIn("route", highest_gap)

        self.loop.run_until_complete(run())

    def test_03_radar_history_snapshots(self):
        async def run():
            history = await SkillRadarService.get_radar_history(self.user_active)
            self.assertGreater(len(history), 0)
            self.assertEqual(history[0]["user_id"], self.user_active)

        self.loop.run_until_complete(run())

if __name__ == "__main__":
    unittest.main()
