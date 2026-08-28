import asyncio
import unittest
from datetime import datetime
from app.services.company_prep_service import CompanyPrepService
from app.repositories.company_prep_repository import company_prep_repository
from app.repositories.resume_repository import resume_repository
from app.repositories.coding_repository import CodingRepository

coding_repo = CodingRepository()

class TestCompanyPrep(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.user_a = f"test_usr_cprep_a_{int(datetime.utcnow().timestamp())}"
        self.user_b = f"test_usr_cprep_b_{int(datetime.utcnow().timestamp())}"

    def test_01_catalog_retrieval(self):
        catalog = CompanyPrepService.get_catalog()
        self.assertIsInstance(catalog, list)
        self.assertGreaterEqual(len(catalog), 10)

        # Check IBM entry
        ibm_entry = next((c for c in catalog if c["id"] == "ibm"), None)
        self.assertIsNotNone(ibm_entry)
        self.assertEqual(ibm_entry["name"], "IBM")
        self.assertIn("Software Engineer", ibm_entry["supported_roles"])

    def test_02_company_prep_plan_generation(self):
        async def run():
            # Save resume scan for user_a
            await resume_repository.save_analysis({
                "user_id": self.user_a,
                "overall_score": 78,
                "matched_keywords": ["Java", "Python", "SQL", "REST APIs"],
                "structured_extraction": {
                    "skills": {
                        "technical": ["Java", "Python", "SQL", "REST APIs"]
                    }
                }
            })

            # Record a coding attempt
            await coding_repo.record_attempt(
                user_id=self.user_a,
                problem_id="p1_two_sum",
                language="python",
                code="def solution(): return True",
                execution_result={"status": "Accepted", "passed_count": 5, "total_count": 5}
            )

            # Get IBM Software Engineer prep plan
            plan = await CompanyPrepService.get_company_prep_plan(self.user_a, "ibm", "Software Engineer")

            self.assertEqual(plan["user_id"], self.user_a)
            self.assertEqual(plan["company"]["id"], "ibm")
            self.assertEqual(plan["target_role"], "Software Engineer")
            self.assertGreater(plan["readiness_summary"]["overall_readiness"], 0)
            self.assertIn("required_skills", plan["skills_analysis"])
            self.assertIn("missing_skills", plan["skills_analysis"])
            self.assertGreater(len(plan["recommended_questions"]), 0)
            self.assertIn("NOTICE:", plan["disclaimer"])

        self.loop.run_until_complete(run())

    def test_03_question_topic_filtering(self):
        async def run():
            # Get Google prep plan (requires Graph Algorithms, Dynamic Programming)
            plan = await CompanyPrepService.get_company_prep_plan(self.user_a, "google", "Software Engineer")
            rec_q = plan["recommended_questions"]

            self.assertIsInstance(rec_q, list)
            self.assertGreater(len(rec_q), 0)
            for q in rec_q:
                self.assertIn("title", q)
                self.assertIn("difficulty", q)

        self.loop.run_until_complete(run())

    def test_04_multi_user_data_isolation(self):
        async def run():
            # User A selects IBM
            await CompanyPrepService.get_company_prep_plan(self.user_a, "ibm", "Software Engineer")

            # User B selects Amazon
            await CompanyPrepService.get_company_prep_plan(self.user_b, "amazon", "Software Engineer")

            doc_a = await company_prep_repository.get_by_user_id(self.user_a)
            doc_b = await company_prep_repository.get_by_user_id(self.user_b)

            self.assertEqual(doc_a["company_id"], "ibm")
            self.assertEqual(doc_b["company_id"], "amazon")
            self.assertNotEqual(doc_a["user_id"], doc_b["user_id"])

        self.loop.run_until_complete(run())

if __name__ == "__main__":
    unittest.main()
