import asyncio
import unittest
from datetime import datetime
from app.services.adaptive_roadmap_service import AdaptiveRoadmapService
from app.repositories.adaptive_roadmap_repository import adaptive_roadmap_repository
from app.repositories.coding_repository import CodingRepository
from app.repositories.resume_repository import resume_repository

coding_repository = CodingRepository()

class TestAdaptiveRoadmap(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.user_a = f"test_usr_a_{int(datetime.utcnow().timestamp())}"
        self.user_b = f"test_usr_b_{int(datetime.utcnow().timestamp())}"

    def test_01_supported_roles_and_templates(self):
        async def run():
            roles = AdaptiveRoadmapService.SUPPORTED_ROLES
            self.assertIn("Software Engineer", roles)
            self.assertIn("Full Stack Developer", roles)
            self.assertIn("Machine Learning Engineer", roles)
            self.assertEqual(len(roles), 11)

            # Test role template retrieval
            se_template = AdaptiveRoadmapService.get_role_template("Software Engineer")
            self.assertTrue(len(se_template) > 0)
            self.assertEqual(se_template[0]["id"], "se_arrays_basics")

        self.loop.run_until_complete(run())

    def test_02_generate_adaptive_roadmap(self):
        async def run():
            config = {
                "target_role": "Full Stack Developer",
                "experience_level": "Entry Level / Fresh Grad",
                "company_type": "MAANG / Tier-1 Product",
                "prep_time_weeks": 4,
                "skill_level": "Intermediate"
            }
            roadmap = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(self.user_a, config)
            self.assertEqual(roadmap["user_id"], self.user_a)
            self.assertEqual(roadmap["config"]["target_role"], "Full Stack Developer")
            self.assertGreater(len(roadmap["items"]), 0)
            self.assertEqual(roadmap["overall_progress"], 0.0)
            self.assertIsNotNone(roadmap["next_recommended_action"])

        self.loop.run_until_complete(run())

    def test_03_weak_skill_prioritization(self):
        async def run():
            # Record a failed coding attempt in a specific topic (e.g. Graphs / Dynamic Programming)
            await coding_repository.record_attempt(
                user_id=self.user_a,
                problem_id="p1_two_sum", # Seed problem
                language="python",
                code="def solution(): return False",
                execution_result={"status": "Wrong Answer", "passed_count": 0, "total_count": 5}
            )

            config = {
                "target_role": "Software Engineer",
                "prep_time_weeks": 4
            }

            roadmap = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(self.user_a, config)
            items = roadmap["items"]

            # Verify items in weak topics have High priority and custom recommendation rationale
            for it in items:
                if "Arrays" in it.get("topic_key", ""):
                    self.assertEqual(it["priority"], "High")
                    self.assertIn("reason_for_recommendation", it)
                    self.assertTrue(len(it["reason_for_recommendation"]) > 0)

        self.loop.run_until_complete(run())

    def test_04_prerequisite_ordering(self):
        async def run():
            config = {"target_role": "Software Engineer"}
            roadmap = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(self.user_a, config)
            items = roadmap["items"]

            item_indices = {it["id"]: idx for idx, it in enumerate(items)}

            # Verify prerequisite items precede dependent items in sequence
            for it in items:
                prereqs = it.get("prerequisites", [])
                for prereq_id in prereqs:
                    if prereq_id in item_indices:
                        self.assertLess(
                            item_indices[prereq_id],
                            item_indices[it["id"]],
                            f"Prerequisite {prereq_id} should appear before {it['id']}"
                        )

        self.loop.run_until_complete(run())

    def test_05_progress_tracking_and_status_toggle(self):
        async def run():
            config = {"target_role": "Software Engineer"}
            roadmap = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(self.user_a, config)
            first_item = roadmap["items"][0]
            item_id = first_item["id"]

            # Toggle status to completed
            updated = await adaptive_roadmap_repository.toggle_item_status(self.user_a, item_id, is_completed=True)
            self.assertIn(item_id, updated["completed_item_ids"])
            self.assertGreater(updated["overall_progress"], 0.0)

            # Toggle status back to uncompleted
            updated_back = await adaptive_roadmap_repository.toggle_item_status(self.user_a, item_id, is_completed=False)
            self.assertNotIn(item_id, updated_back["completed_item_ids"])
            self.assertEqual(updated_back["overall_progress"], 0.0)

        self.loop.run_until_complete(run())

    def test_06_dynamic_recalculation_preserves_completed_progress(self):
        async def run():
            config = {"target_role": "Software Engineer"}
            roadmap = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(self.user_a, config)
            first_item_id = roadmap["items"][0]["id"]

            # Mark item completed
            await adaptive_roadmap_repository.toggle_item_status(self.user_a, first_item_id, is_completed=True)

            # Recalculate roadmap
            recalculated = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(self.user_a, config)
            self.assertIn(first_item_id, recalculated["completed_item_ids"])
            
            # Verify status is preserved as completed
            item_status = next(it["completion_status"] for it in recalculated["items"] if it["id"] == first_item_id)
            self.assertEqual(item_status, "completed")

        self.loop.run_until_complete(run())

    def test_07_user_data_isolation(self):
        async def run():
            config_a = {"target_role": "Software Engineer"}
            config_b = {"target_role": "Data Engineer"}

            roadmap_a = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(self.user_a, config_a)
            roadmap_b = await AdaptiveRoadmapService.generate_or_recalculate_roadmap(self.user_b, config_b)

            # Toggle user_a's first item
            item_a_id = roadmap_a["items"][0]["id"]
            await adaptive_roadmap_repository.toggle_item_status(self.user_a, item_a_id, is_completed=True)

            fetched_b = await adaptive_roadmap_repository.get_by_user_id(self.user_b)
            self.assertNotIn(item_a_id, fetched_b.get("completed_item_ids", []))
            self.assertEqual(fetched_b["config"]["target_role"], "Data Engineer")

        self.loop.run_until_complete(run())

if __name__ == "__main__":
    unittest.main()
