from typing import Dict, Any, List
from app.services.code_executor import CodeExecutor
from app.data.problems_seed import ARENA_CATEGORIES_DATA

def validate_problem(problem: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates a coding problem definition:
    1. Checks required fields (id, title, description, difficulty, roles, visible_test_cases, hidden_test_cases, reference_solution)
    2. Runs reference solution against visible and hidden test cases.
    3. Confirms reference solution achieves ACCEPTED status.
    """
    required_fields = ["id", "title", "description", "difficulty", "roles", "visible_test_cases", "hidden_test_cases", "reference_solution"]
    missing = [field for field in required_fields if field not in problem or problem[field] is None]
    if missing:
        return {
            "valid": False,
            "problem_id": problem.get("id", "unknown"),
            "error": f"Missing required fields: {', '.join(missing)}"
        }

    ref_sol = problem["reference_solution"]
    all_tests = problem.get("visible_test_cases", []) + problem.get("hidden_test_cases", [])

    if not all_tests:
        return {
            "valid": False,
            "problem_id": problem["id"],
            "error": "Problem has no test cases configured."
        }

    # Evaluate reference solution using Python runtime
    eval_res = CodeExecutor.evaluate(code=ref_sol, language="python", test_cases=all_tests, timeout_per_test=3.0)

    if eval_res["status"] != "ACCEPTED":
        return {
            "valid": False,
            "problem_id": problem["id"],
            "error": f"Reference solution failed validation with verdict: {eval_res['status']} ({eval_res['passed_tests']}/{eval_res['total_tests']} passed)."
        }

    return {
        "valid": True,
        "problem_id": problem["id"],
        "passed_tests": eval_res["passed_tests"],
        "total_tests": eval_res["total_tests"]
    }

def validate_all_seed_problems() -> List[Dict[str, Any]]:
    """Validates all problems in ARENA_CATEGORIES_DATA."""
    results = []
    for cat in ARENA_CATEGORIES_DATA:
        for top in cat["topics"]:
            for problem in top["problems"]:
                res = validate_problem(problem)
                results.append(res)
    return results

if __name__ == "__main__":
    validation_report = validate_all_seed_problems()
    valid_count = sum(1 for r in validation_report if r["valid"])
    print(f"Validated {valid_count}/{len(validation_report)} seed problems successfully.")
