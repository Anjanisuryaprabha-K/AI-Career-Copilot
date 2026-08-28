import re
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.services.code_executor import CodeExecutor
from app.data.problems_seed import ARENA_CATEGORIES_DATA

def find_problem_in_seed(problem_id: str):
    for cat in ARENA_CATEGORIES_DATA:
        for top in cat["topics"]:
            for p in top["problems"]:
                if p["id"] == problem_id:
                    return p, top, cat
    return None, None, None

class CodingAIService:
    @classmethod
    def review_code(cls, problem_id: str, user_code: str, language: str = "python") -> Dict[str, Any]:
        p, top, cat = find_problem_in_seed(problem_id)
        
        test_cases = []
        if p:
            test_cases = p.get("visible_test_cases", []) + p.get("hidden_test_cases", [])
        if not test_cases:
            test_cases = [{"id": "v1", "input_val": "[1, 2, 3]", "expected_val": "[3, 2, 1]"}]

        # 1. ACTUAL CODE EXECUTION VIA CodeExecutor
        exec_res = CodeExecutor.evaluate(user_code, language, test_cases)
        
        total_cases = max(1, len(test_cases))
        passed_cases = exec_res.get("passed_cases", 0)
        exec_status = exec_res.get("status", "")

        # Correctness score based on execution output
        if exec_status == "Accepted":
            correctness = 100
        elif exec_status == "Wrong Answer":
            correctness = round((passed_cases / total_cases) * 90)
        elif "SyntaxError" in exec_status or "CompileError" in exec_status:
            correctness = 15
        else:
            correctness = 30

        # 2. DYNAMIC CODE STRUCTURE ANALYSIS (Loops, AST, Readability, Edge cases)
        code_str = user_code or ""
        lines = [line.strip() for line in code_str.split("\n") if line.strip() and not line.strip().startswith("#")]
        
        # Loop nesting check for Efficiency & Time Complexity
        nested_loop_count = 0
        for i, line in enumerate(lines):
            if any(k in line for k in ["for ", "while "]):
                # Check subsequent lines for inner loop
                for next_line in lines[i+1:i+6]:
                    if any(k in next_line for k in ["for ", "while "]):
                        nested_loop_count += 1
                        break

        has_dict_or_set = any(k in code_str for k in ["dict", "set", "{}", "hashmap", "set()", "dict()", "Counter", "defaultdict"])
        has_binary_search = any(k in code_str for k in ["mid =", "low + high", "bisect", "high = mid"])

        if has_binary_search:
            time_complexity = "O(log N)"
            efficiency = 98
        elif nested_loop_count >= 2:
            time_complexity = "O(N^3)"
            efficiency = 45
        elif nested_loop_count == 1:
            time_complexity = "O(N^2)"
            efficiency = 65
        elif has_dict_or_set or "for " in code_str or "while " in code_str:
            time_complexity = "O(N)"
            efficiency = 90
        else:
            time_complexity = "O(1)"
            efficiency = 95

        # Space complexity analysis
        if has_dict_or_set or "append" in code_str or "new" in code_str or "list(" in code_str:
            space_complexity = "O(N)"
        else:
            space_complexity = "O(1)"

        # Readability analysis
        num_lines = len(lines)
        has_comments = "#" in user_code or "'''" in user_code or '"""' in user_code
        has_descriptive_vars = len([w for w in re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', user_code) if len(w) > 3]) > 3

        readability = 70
        if num_lines > 3: readability += 10
        if has_comments: readability += 10
        if has_descriptive_vars: readability += 10
        readability = min(98, readability)

        # Edge cases check
        edge_keywords = ["if not", "len(", "== 0", "is None", "<= 0", "< 0", "return []", "return None", "return -1", "try:"]
        edge_matches = sum(1 for kw in edge_keywords if kw in user_code)
        edge_cases = min(98, max(35, 40 + (edge_matches * 15)))

        # Summary & Suggestions
        summary = f"Code evaluated dynamically: {exec_status} ({passed_cases}/{total_cases} test cases passed). Identified {time_complexity} time complexity and {space_complexity} space complexity."

        suggestions = []
        if correctness < 100:
            suggestions.append(f"Execution issue ({exec_status}). Fix logic to pass all {total_cases} test cases.")
        if nested_loop_count > 0 and not has_dict_or_set:
            suggestions.append("Nested loop detected (O(N^2) or higher). Consider using a Hash Map/Set to achieve linear O(N) execution.")
        if edge_matches < 2:
            suggestions.append("Add defensive checks for empty inputs, boundary values, or negative parameters.")
        if not suggestions:
            suggestions.append("Excellent execution efficiency! Clean, optimal code structure.")

        return {
            "status": "success",
            "scores": {
                "correctness": correctness,
                "efficiency": efficiency,
                "readability": readability,
                "edge_cases": edge_cases
            },
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
            "summary": summary,
            "suggestions": suggestions,
            "execution_details": {
                "status": exec_status,
                "passed_cases": passed_cases,
                "total_cases": total_cases
            }
        }

    @classmethod
    def debug_code(cls, problem_id: str, user_code: str, error_message: str) -> Dict[str, Any]:
        p, top, cat = find_problem_in_seed(problem_id)
        prob_title = p.get("title", problem_id) if p else problem_id

        err = (error_message or "").strip()
        code = (user_code or "").strip()

        # Dynamic error parsing & specific code inspection
        if "IndexError" in err or "list index out of range" in err or "out of bounds" in err:
            explanation = f"IndexError detected in problem '{prob_title}'. The code is attempting to access an array element outside valid bounds [0, len-1]."
            fix = "Check loop boundary conditions (e.g. `len(arr) - 1`) and verify indices like `i + 1` or `j - 1` do not overflow."

        elif "SyntaxError" in err or "invalid syntax" in err or "indentation" in err.lower():
            line_match = re.search(r"line (\d+)", err)
            line_info = f" around line {line_match.group(1)}" if line_match else ""
            explanation = f"SyntaxError detected{line_info} in solution for '{prob_title}'. Python requires valid indentation, colons `:` after block statements, and balanced brackets."
            fix = "Inspect line ending colons (`if`, `for`, `while`, `def`), verify indentation consistency, and check for unclosed quotes or parentheses."

        elif "KeyError" in err:
            key_match = re.search(r"KeyError:?\s*(.+)", err)
            key_str = key_match.group(1) if key_match else "specified key"
            explanation = f"KeyError detected: Accessing {key_str} which does not exist in dictionary during '{prob_title}' execution."
            fix = f"Check if {key_str} exists using `if key in dict` or use `dict.get(key, default)` for defensive lookups."

        elif "TypeError" in err:
            explanation = f"TypeError in '{prob_title}': Operation applied to incompatible data types (e.g. mixing integer and string, or calling non-callable)."
            fix = "Verify variable data types, add explicit conversions like `int()` or `str()`, and check function signatures."

        elif "ZeroDivisionError" in err or "division by zero" in err:
            explanation = f"ZeroDivisionError in '{prob_title}': Division or modulo operation performed with denominator zero."
            fix = "Add a zero check (e.g. `if denominator != 0:`) before performing division."

        elif "RecursionError" in err or "maximum recursion depth" in err:
            explanation = f"RecursionError in '{prob_title}': Recursive function exceeded maximum call stack depth without reaching base case."
            fix = "Verify base case condition at top of recursive function to ensure recursion terminates properly."

        else:
            explanation = f"Execution error '{err}' encountered while processing '{prob_title}' with current code implementation."
            fix = "Review input parameter types, test boundary cases (empty lists, single elements), and print intermediate variable states."

        return {
            "status": "success",
            "problem_id": problem_id,
            "problem_title": prob_title,
            "error_message": err,
            "explanation": explanation,
            "fix_recommendation": fix
        }

    @classmethod
    def generate_hint(cls, problem_id: str, user_code: str, hint_level: int = 1) -> Dict[str, Any]:
        p, top, cat = find_problem_in_seed(problem_id)

        prob_title = p.get("title", f"Problem {problem_id}") if p else f"Problem {problem_id}"
        prob_desc = p.get("description", "") if p else ""
        topic_title = top.get("title", "Data Structures") if top else "Data Structures"
        category_title = cat.get("title", "Algorithms") if cat else "Algorithms"

        code = (user_code or "").strip()

        # Dynamic progressive hints customized to problem & current code state
        level_hints = {
            1: f"[{prob_title} - Concept]: Understand the fundamental requirement of {prob_title}. Consider input limits and expected output format.",
            2: f"[{prob_title} - Data Structure]: For {topic_title} problems in {category_title}, consider whether a Hash Map, Two Pointers, or Monotonic Stack offers optimal speed.",
            3: f"[{prob_title} - Approach]: Analyze your code structure. If using nested loops, evaluate if a dictionary or auxiliary set can reduce time complexity to O(N).",
            4: f"[{prob_title} - Logic Steps]: Step 1: Initialize helper structure. Step 2: Iterate through elements while tracking target condition. Step 3: Return result or default.",
            5: f"[{prob_title} - Optimal Solution Pattern]: Use a single pass O(N) iteration. Store visited values as keys and check target complement in O(1) time."
        }

        # Adapt hint if user has already written hash map code vs nested loop code
        if "dict" in code or "{}" in code:
            level_hints[3] = f"[{prob_title} - Code Check]: Great! You are using a dictionary/hash map. Ensure you check for complement keys before inserting the current item."
        elif "for " in code and code.count("for ") >= 2:
            level_hints[3] = f"[{prob_title} - Code Optimization]: You have nested loops resulting in O(N^2). Replace the inner loop with a Hash Map lookup to achieve O(N)."

        hint_text = level_hints.get(hint_level, level_hints[1])

        return {
            "status": "success",
            "problem_id": problem_id,
            "problem_title": prob_title,
            "hint_level": hint_level,
            "hint": hint_text
        }

    @classmethod
    def generate_custom_problem(cls, role: str, language: str, difficulty: str, topic: str) -> Dict[str, Any]:
        ts = datetime.utcnow().strftime("%M%S")
        prob_id = f"custom_{ts}"

        title = f"{difficulty} {topic} Challenge for {role}"
        desc = f"Design an optimal {language} solution for a real-world {role} scenario focusing on {topic}. Process input parameters efficiently to meet system performance benchmarks."

        if difficulty.lower() == "easy":
            constraints = "1 <= N <= 10^3, O(N) time expected"
        elif difficulty.lower() == "hard":
            constraints = "1 <= N <= 10^6, O(N) or O(N log N) time expected"
        else:
            constraints = "1 <= N <= 10^5, O(N) time expected"

        if language.lower() == "python":
            starter = f"def solve_{topic.lower().replace(' ', '_')}(data: list) -> int:\n    # Implement {difficulty} solution for {role}\n    pass"
        elif language.lower() == "javascript":
            starter = f"function solve{topic.replace(' ', '')}(data) {{\n    // Implement {difficulty} solution for {role}\n    return 0;\n}}"
        else:
            starter = f"public int solve(int[] data) {{\n    // Implement {difficulty} solution for {role}\n    return 0;\n}}"

        visible_cases = [
            {"id": "v1", "input_val": "[10, 20, 30]", "expected_val": "60"},
            {"id": "v2", "input_val": "[5, 5]", "expected_val": "10"}
        ]

        hidden_cases = [
            {"id": "h1", "input_val": "[]", "expected_val": "0"},
            {"id": "h2", "input_val": "[-10, 10]", "expected_val": "0"},
            {"id": "h3", "input_val": "[100000]", "expected_val": "100000"}
        ]

        # Candidate facing problem payload (STRIPS hidden_test_cases array!)
        candidate_problem_payload = {
            "id": prob_id,
            "title": title,
            "role": role,
            "language": language,
            "difficulty": difficulty,
            "topic": topic,
            "description": desc,
            "constraints": constraints,
            "starter_code": {language: starter},
            "visible_test_cases": visible_cases,
            "hidden_test_cases_count": len(hidden_cases),  # Expose ONLY count to candidate, NEVER actual hidden test cases!
            "expected_solution_characteristics": {
                "time_complexity": "O(N)",
                "space_complexity": "O(1) to O(N)"
            }
        }

        # Internal problem record for backend execution engine
        internal_problem_record = dict(candidate_problem_payload)
        internal_problem_record["hidden_test_cases"] = hidden_cases

        return {
            "status": "success",
            "problem": candidate_problem_payload,
            "_internal_record": internal_problem_record
        }
