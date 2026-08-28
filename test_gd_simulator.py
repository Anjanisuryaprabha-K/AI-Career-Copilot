import asyncio
import unittest
from datetime import datetime
from app.services.gd_service import GDService
from app.repositories.gd_repository import gd_repository

class TestGDSimulator(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.user_a = f"test_usr_gd_a_{int(datetime.utcnow().timestamp())}"
        self.user_b = f"test_usr_gd_b_{int(datetime.utcnow().timestamp())}"

    def test_01_empty_and_short_response_handling(self):
        async def run():
            # Test empty transcript
            res_empty = await GDService.evaluate_gd_session(
                user_id=self.user_a,
                topic_title="Is Remote Work Accelerating Tech Innovation?",
                category="Technology",
                difficulty="Medium",
                duration_minutes=5,
                user_transcript=""
            )
            self.assertEqual(res_empty["status"], "error")
            self.assertIn("empty", res_empty["error"].lower())

            # Test short transcript under 10 chars
            res_short = await GDService.evaluate_gd_session(
                user_id=self.user_a,
                topic_title="Is Remote Work Accelerating Tech Innovation?",
                category="Technology",
                difficulty="Medium",
                duration_minutes=5,
                user_transcript="Hi"
            )
            self.assertEqual(res_short["status"], "error")

        self.loop.run_until_complete(run())

    def test_02_gd_score_calculation_and_non_diagnostic_wording(self):
        async def run():
            valid_transcript = (
                "Building on Alex and Priya's points, I strongly agree that remote work enhances developer focus time. "
                "However, we must establish clear asynchronous communication channels to maintain team alignment and mentorship."
            )
            res = await GDService.evaluate_gd_session(
                user_id=self.user_a,
                topic_title="Is Remote Work Accelerating Tech Innovation?",
                category="Technology",
                difficulty="Medium",
                duration_minutes=5,
                user_transcript=valid_transcript
            )

            self.assertEqual(res["status"], "success")
            sess = res["session"]

            # Verify score is within 0-100 range
            self.assertGreaterEqual(sess["gd_score"], 0)
            self.assertLessEqual(sess["gd_score"], 100)

            # Verify 7 components present in score breakdown
            breakdown = sess["score_breakdown"]
            self.assertIn("communication", breakdown)
            self.assertIn("content_and_arguments", breakdown)
            self.assertIn("relevance", breakdown)
            self.assertIn("confidence_indicators", breakdown)
            self.assertIn("structure_and_conclusion", breakdown)
            self.assertIn("listening_and_response_quality", breakdown)
            self.assertIn("speech_delivery_prosody", breakdown)

            # Verify non-diagnostic wording
            conf_text = sess["non_diagnostic_indicators"]["confidence_indicator"]
            self.assertIn("speech delivery characteristics indicate", conf_text.lower())
            self.assertNotIn("you are anxious", conf_text.lower())

        self.loop.run_until_complete(run())

    def test_03_user_data_isolation_and_history(self):
        async def run():
            # Save session for User A
            await GDService.evaluate_gd_session(
                user_id=self.user_a,
                topic_title="Generative AI in Software Engineering",
                category="AI",
                difficulty="Hard",
                duration_minutes=5,
                user_transcript="AI tools assist developers by generating boilerplate code while engineers focus on high-level architecture."
            )

            # Save session for User B
            await GDService.evaluate_gd_session(
                user_id=self.user_b,
                topic_title="Green Computing & Carbon Neutrality",
                category="Environment",
                difficulty="Medium",
                duration_minutes=5,
                user_transcript="Data center energy efficiency can be improved using renewable power contracts and advanced cooling systems."
            )

            # Fetch history for User A
            hist_a = await GDService.get_user_gd_history(self.user_a)
            hist_b = await GDService.get_user_gd_history(self.user_b)

            self.assertGreaterEqual(len(hist_a), 1)
            self.assertGreaterEqual(len(hist_b), 1)

            # Verify User A's history does NOT contain User B's topics
            for s in hist_a:
                self.assertEqual(s["user_id"], str(self.user_a))
                self.assertNotEqual(s["category"], "Environment")

        self.loop.run_until_complete(run())

    def test_04_simulated_participants_and_topic_generation(self):
        async def run():
            categories = GDService.get_categories()
            self.assertIn("Technology", categories)
            self.assertIn("Software Industry", categories)

            topics = GDService.get_topics(category="AI")
            self.assertGreater(len(topics), 0)

            participants = GDService.generate_simulated_participants(topics[0]["title"], "AI")
            self.assertEqual(len(participants), 3)

        self.loop.run_until_complete(run())

if __name__ == "__main__":
    unittest.main()
