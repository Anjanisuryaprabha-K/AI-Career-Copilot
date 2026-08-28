import asyncio
import unittest
from datetime import datetime
from app.services.adaptive_coding_engine import AdaptiveCodingEngine
from app.repositories.coding_repository import CodingRepository

coding_repo = CodingRepository()

class TestAdaptiveCodingEngine(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.user_a = f"test_usr_adapt_a_{int(datetime.utcnow().timestamp())}"
        self.user_b = f"test_usr_adapt_b_{int(datetime.utcnow().timestamp())}"

    def test_01_difficulty_adaptation(self):
        async def run():
            # Initially, zero solved questions -> Stage Easy
            profile_init = await AdaptiveCodingEngine.get_user_coding_profile(self.user_a)
            self.assertEqual(profile_init["target_difficulty"], "Easy")

            # Simulate candidate solving 3 Easy questions
            await coding_repo.record_attempt(
                user_id=self.user_a,
                problem_id="arr_01_reverse",
                language="python",
                code="def sol(): pass",
                execution_result={"status": "Accepted", "passed_count": 5, "total_count": 5}
            )
            await coding_repo.update_arena_progress(self.user_a, "arr_01_reverse", "arrays_basics", 2)

            await coding_repo.record_attempt(
                user_id=self.user_a,
                problem_id="arr_02_max_sub",
                language="python",
                code="def sol(): pass",
                execution_result={"status": "Accepted", "passed_count": 5, "total_count": 5}
            )
            await coding_repo.update_arena_progress(self.user_a, "arr_02_max_sub", "arrays_basics", 2)

            # Re-evaluate profile -> Elevates to Medium
            profile_elevated = await AdaptiveCodingEngine.get_user_coding_profile(self.user_a)
            self.assertIn(profile_elevated["target_difficulty"], ["Medium", "Hard"])

        self.loop.run_until_complete(run())

    def test_02_solved_question_exclusion(self):
        async def run():
            # Mark 'arr_01_reverse' as solved for user_b
            await coding_repo.record_attempt(
                user_id=self.user_b,
                problem_id="arr_01_reverse",
                language="python",
                code="def sol(): pass",
                execution_result={"status": "Accepted", "passed_count": 5, "total_count": 5}
            )
            await coding_repo.update_arena_progress(self.user_b, "arr_01_reverse", "arrays_basics", 2)

            # Get next adaptive problem for user_b
            res = await AdaptiveCodingEngine.get_next_adaptive_problem(self.user_b)
            next_p = res["next_problem"]

            # Verify solved question is NOT recommended
            self.assertNotEqual(next_p["id"], "arr_01_reverse")

        self.loop.run_until_complete(run())

    def test_03_adaptive_queue_laddering(self):
        async def run():
            queue = await AdaptiveCodingEngine.get_adaptive_queue(self.user_a, limit=5)
            self.assertIsInstance(queue, list)
            self.assertGreater(len(queue), 0)
            
            # Check ladder ordering tags
            for idx, item in enumerate(queue):
                self.assertEqual(item["adaptive_step"], idx + 1)
                self.assertIn("Step", item["ladder_level"])

        self.loop.run_until_complete(run())

    def test_04_multi_user_isolation(self):
        async def run():
            profile_a = await AdaptiveCodingEngine.get_user_coding_profile(self.user_a)
            profile_b = await AdaptiveCodingEngine.get_user_coding_profile(self.user_b)

            self.assertNotEqual(profile_a["user_id"], profile_b["user_id"])

        self.loop.run_until_complete(run())

if __name__ == "__main__":
    unittest.main()
