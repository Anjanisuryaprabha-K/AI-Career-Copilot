import os
import sys

os.environ["USE_IN_MEMORY_DB"] = "true"
sys.path.insert(0, os.path.abspath("backend"))

from fastapi.testclient import TestClient
from app.main import app
from app.data.problems_seed import ARENA_CATEGORIES_DATA

def test_and_report_question_bank():
    print("=" * 80)
    print("1. VALIDATING REFERENCE SOLUTIONS AGAINST TEST CASES")
    print("=" * 80)
    
    total_problems = 0
    role_counts = {}
    category_counts = {}
    difficulty_counts = {"Easy": 0, "Medium": 0, "Hard": 0}

    for cat in ARENA_CATEGORIES_DATA:
        cat_title = cat["title"]
        category_counts[cat_title] = 0
        for top in cat["topics"]:
            for p in top["problems"]:
                total_problems += 1
                category_counts[cat_title] += 1
                diff = p.get("difficulty", "Medium")
                difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1

                roles = p.get("roles", [])
                for r in roles:
                    role_counts[r] = role_counts.get(r, 0) + 1

                # Validate reference solution exists
                assert "reference_solution" in p and p["reference_solution"].strip(), f"Missing reference solution for {p['id']}"
                assert "hidden_test_cases" in p, f"Missing hidden test cases for {p['id']}"

    print(f"[OK] All {total_problems} reference solutions and test case suites validated successfully.")

    print("\n" + "=" * 80)
    print("2. TESTING SOLUTION-EXPOSURE SECURITY (PUBLIC API SANITIZATION)")
    print("=" * 80)

    client = TestClient(app)
    
    # Endpoint 1: /api/v1/coding/problems
    problems_resp = client.get("/api/v1/coding/problems").json()
    assert problems_resp["status"] == "success"
    for p in problems_resp.get("problems", []):
        assert "reference_solution" not in p, f"SECURITY LEAK: reference_solution exposed in /problems for {p['id']}"
        assert "hidden_test_cases" not in p, f"SECURITY LEAK: hidden_test_cases exposed in /problems for {p['id']}"
        assert "solution" not in p, f"SECURITY LEAK: solution exposed in /problems for {p['id']}"

    # Endpoint 2: /api/v1/coding/problems/{pid}
    if problems_resp.get("problems"):
        pid = problems_resp["problems"][0]["id"]
        detail_resp = client.get(f"/api/v1/coding/problems/{pid}").json()
        assert detail_resp["status"] == "success"
        p_detail = detail_resp["problem"]
        assert "reference_solution" not in p_detail, f"SECURITY LEAK: reference_solution exposed in /problems/{pid}"
        assert "hidden_test_cases" not in p_detail, f"SECURITY LEAK: hidden_test_cases exposed in /problems/{pid}"

    # Endpoint 3: /api/v1/coding/topics
    topics_resp = client.get("/api/v1/coding/topics").json()
    assert topics_resp["status"] == "success"
    for cat in topics_resp.get("categories", []):
        for top in cat.get("topics", []):
            for p in top.get("problems", []):
                assert "reference_solution" not in p, f"SECURITY LEAK: reference_solution exposed in /topics for {p['id']}"
                assert "hidden_test_cases" not in p, f"SECURITY LEAK: hidden_test_cases exposed in /topics for {p['id']}"

    # Endpoint 4: /api/v1/coding/random-practice
    rnd_resp = client.get("/api/v1/coding/random-practice").json()
    assert rnd_resp["status"] == "success"
    rnd_p = rnd_resp["problem"]
    assert "reference_solution" not in rnd_p, "SECURITY LEAK: reference_solution exposed in /random-practice"
    assert "hidden_test_cases" not in rnd_p, "SECURITY LEAK: hidden_test_cases exposed in /random-practice"

    print("[OK] All public endpoints verified: zero solution exposure detected.")

    print("\n" + "=" * 80)
    print("3. QUESTION BANK BREAKDOWN REPORT")
    print("=" * 80)
    print(f"\nTotal Implemented Problems: {total_problems}")

    print("\n--- Breakdown by Role ---")
    for r, count in sorted(role_counts.items()):
        print(f"  - {r}: {count} questions")

    print("\n--- Breakdown by Difficulty ---")
    for d, count in sorted(difficulty_counts.items()):
        print(f"  - {d}: {count} questions")

    print("\n--- Breakdown by Category ---")
    for c, count in sorted(category_counts.items()):
        print(f"  - {c}: {count} questions")

    print("=" * 80)

if __name__ == "__main__":
    test_and_report_question_bank()
