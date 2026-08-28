import os
import sys
import time
import shutil

os.environ["USE_IN_MEMORY_DB"] = "true"
sys.path.insert(0, os.path.abspath("backend"))

from app.services.code_executor import CodeExecutor
from app.utils.problem_validator import validate_problem

def test_compiler_scenarios():
    print("=" * 80)
    print("TESTING HARDENED CODING ARENA COMPILER & EXECUTION ENGINE")
    print("=" * 80)

    # 1. Correct Python Solution -> ACCEPTED
    py_code = "def reverse_string(s: str) -> str:\n    return s[::-1]"
    res1 = CodeExecutor.evaluate(
        code=py_code,
        language="python",
        test_cases=[
            {"input_val": "'hello'", "expected_val": "'olleh'"},
            {"input_val": "'world'", "expected_val": "'dlrow'"}
        ]
    )
    assert res1["status"] == "ACCEPTED", f"Scenario 1 failed: {res1}"
    assert res1["passed_tests"] == 2
    print("[OK] 1. Correct Python solution -> ACCEPTED")

    # 2. Wrong Python Solution -> WRONG_ANSWER
    py_wrong = "def reverse_string(s: str) -> str:\n    return s"
    res2 = CodeExecutor.evaluate(
        code=py_wrong,
        language="python",
        test_cases=[{"input_val": "'hello'", "expected_val": "'olleh'"}]
    )
    assert res2["status"] == "WRONG_ANSWER", f"Scenario 2 failed: {res2}"
    print("[OK] 2. Wrong solution -> WRONG_ANSWER")

    # 3. Syntax Error -> RUNTIME_ERROR / COMPILATION_ERROR
    py_syntax = "def reverse_string(s: str) -> str:\n    return s[::-1"
    res3 = CodeExecutor.evaluate(
        code=py_syntax,
        language="python",
        test_cases=[{"input_val": "'hello'", "expected_val": "'olleh'"}]
    )
    assert res3["status"] in ["RUNTIME_ERROR", "COMPILATION_ERROR"], f"Scenario 3 failed: {res3}"
    print("[OK] 3. Syntax error -> RUNTIME_ERROR / COMPILATION_ERROR")

    # 4. Runtime Exception (Division by Zero) -> RUNTIME_ERROR
    py_divzero = "def div_zero(nums):\n    return 1 / 0"
    res4 = CodeExecutor.evaluate(
        code=py_divzero,
        language="python",
        test_cases=[{"input_val": "[1, 2]", "expected_val": "0"}]
    )
    assert res4["status"] == "RUNTIME_ERROR", f"Scenario 4 failed: {res4}"
    assert "ZeroDivisionError" in res4["runtime_output"] or "ZeroDivisionError" in res4["test_details"][0].get("error", "")
    print("[OK] 4. Runtime exception (Division by zero) -> RUNTIME_ERROR")

    # 5. Infinite Loop -> TIME_LIMIT_EXCEEDED
    py_infloop = "def inf_loop(n):\n    while True: pass"
    res5 = CodeExecutor.evaluate(
        code=py_infloop,
        language="python",
        test_cases=[{"input_val": "5", "expected_val": "5"}],
        timeout_per_test=1.0
    )
    assert res5["status"] == "TIME_LIMIT_EXCEEDED", f"Scenario 5 failed: {res5}"
    print("[OK] 5. Infinite loop -> TIME_LIMIT_EXCEEDED (Process killed)")

    # 6. Whitespace Differences ("1 2 3" vs "1 2 3\n") -> ACCEPTED
    assert CodeExecutor.compare_outputs("1 2 3\n", "1 2 3") is True
    assert CodeExecutor.compare_outputs("1 2\r\n", "1 2") is True
    assert CodeExecutor.compare_outputs("1 2", "1 3") is False
    print("[OK] 6. Output comparison (whitespace & newlines) verified")

    # 7. Unsupported / Unavailable Language -> LANGUAGE_UNAVAILABLE
    res7 = CodeExecutor.evaluate(
        code="print('hi')",
        language="brainfuck_unsupported",
        test_cases=[{"input_val": "", "expected_val": ""}]
    )
    assert res7["status"] == "LANGUAGE_UNAVAILABLE", f"Scenario 7 failed: {res7}"
    print("[OK] 7. Unavailable language -> LANGUAGE_UNAVAILABLE")

    # 8. Empty Code -> COMPILATION_ERROR
    res8 = CodeExecutor.evaluate(
        code="    \n   ",
        language="python",
        test_cases=[{"input_val": "1", "expected_val": "1"}]
    )
    assert res8["status"] == "COMPILATION_ERROR", f"Scenario 8 failed: {res8}"
    print("[OK] 8. Empty code -> COMPILATION_ERROR")

    # 9. Path Sanitization Check
    clean_err = CodeExecutor.sanitize_error("File 'C:\\Users\\Secrets\\tmp\\solution.py', line 2", "C:\\Users\\Secrets\\tmp")
    assert "C:\\Users\\Secrets\\tmp" not in clean_err
    print("[OK] 9. Error path sanitization verified")

    # 10. Problem Validation Utility Check
    sample_problem = {
        "id": "arr_01_reverse",
        "title": "Reverse an Array",
        "description": "Reverse an array in place.",
        "difficulty": "Easy",
        "roles": ["Software Engineer"],
        "visible_test_cases": [{"input_val": "[1, 2, 3]", "expected_val": "[3, 2, 1]"}],
        "hidden_test_cases": [{"input_val": "[5, 4]", "expected_val": "[4, 5]"}],
        "reference_solution": "def reverse_list(nums):\n    return nums[::-1]"
    }
    val_res = validate_problem(sample_problem)
    assert val_res["valid"] is True, f"Problem validation failed: {val_res}"
    print("[OK] 10. Problem Validation Utility verified")

    print("=" * 80)
    print("ALL COMPILER & EXECUTION ENGINE TESTS PASSED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    test_compiler_scenarios()
