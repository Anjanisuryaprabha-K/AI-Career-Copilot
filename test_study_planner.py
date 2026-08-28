import asyncio
import unittest
from datetime import datetime
from app.services.study_planner_service import StudyPlannerService

class TestStudyPlanner(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.user_a = f"test_usr_planner_a_{int(datetime.utcnow().timestamp())}"
        self.user_b = f"test_usr_planner_b_{int(datetime.utcnow().timestamp())}"

    def test_01_generate_schedule_and_target_interview_date(self):
        async def run():
            config = {
                "target_role": "Software Engineer",
                "target_company": "Amazon",
                "interview_date": "2026-09-15",
                "available_hours_per_day": 2,
                "days_per_week": 5,
                "preferred_study_time": "Evening",
                "current_skill_level": "Intermediate"
            }
            plan = await StudyPlannerService.generate_study_plan(self.user_a, config)
            self.assertEqual(plan["target_role"], "Software Engineer")
            self.assertEqual(plan["target_company"], "Amazon")
            self.assertTrue(len(plan["days_schedule"]) > 0)
            
            # Verify direct feature route links attached to tasks
            first_task = plan["days_schedule"][0]["tasks"][0]
            self.assertIn("/coding-arena", first_task["route"])

        self.loop.run_until_complete(run())

    def test_02_task_completion_and_rescheduling(self):
        async def run():
            plan = await StudyPlannerService.get_user_study_plan(self.user_a)
            task = plan["days_schedule"][0]["tasks"][0]
            task_id = task["task_id"]

            res_comp = await StudyPlannerService.complete_task(self.user_a, task_id)
            self.assertEqual(res_comp["status"], "success")
            self.assertGreater(res_comp["completion_percentage"], 0)

            # Reschedule remaining pending tasks
            res_resched = await StudyPlannerService.reschedule_missed_tasks(self.user_a)
            self.assertEqual(res_resched["status"], "success")

        self.loop.run_until_complete(run())

    def test_03_user_isolation(self):
        async def run():
            plan_a = await StudyPlannerService.get_user_study_plan(self.user_a)
            plan_b = await StudyPlannerService.get_user_study_plan(self.user_b)

            self.assertEqual(plan_a["user_id"], self.user_a)
            self.assertEqual(plan_b["user_id"], self.user_b)

        self.loop.run_until_complete(run())

if __name__ == "__main__":
    unittest.main()
