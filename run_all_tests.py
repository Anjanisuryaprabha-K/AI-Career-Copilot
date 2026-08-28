import os
import sys
import subprocess
import json

python_exe = r"C:\Users\Satish preetham\AppData\Local\Programs\Python\Python312\python.exe"

test_files = [
    "test_health.py",
    "test_mongo.py",
    "test_adaptive_coding_engine.py",
    "test_adaptive_roadmap.py",
    "test_coding_arena_report.py",
    "test_coding_executor.py",
    "test_company_prep.py",
    "test_gd_simulator.py",
    "test_mongodb_persistence_and_isolation.py",
    "test_placement_mentor.py",
    "test_skill_radar.py",
    "test_study_planner.py",
    "test_weakness_detector.py",
    "test_suite_runner.py"
]

results = []

env = os.environ.copy()
env["USE_IN_MEMORY_DB"] = "true"
env["PYTHONPATH"] = os.path.abspath("backend")

print("Starting test execution...")

for test_file in test_files:
    test_path = os.path.abspath(test_file)
    if not os.path.exists(test_path):
        results.append({"file": test_file, "status": "SKIPPED", "error": "File not found"})
        continue
    
    print(f"Running {test_file}...")
    try:
        proc = subprocess.run(
            [python_exe, test_path],
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
            cwd=os.path.abspath(".")
        )
        passed = (proc.returncode == 0)
        results.append({
            "file": test_file,
            "status": "PASSED" if passed else "FAILED",
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr
        })
        print(f"  Result: {'PASSED' if passed else 'FAILED'}")
    except subprocess.TimeoutExpired as te:
        results.append({
            "file": test_file,
            "status": "TIMEOUT",
            "error": "Timed out after 30 seconds"
        })
        print(f"  Result: TIMEOUT")
    except Exception as e:
        results.append({
            "file": test_file,
            "status": "ERROR",
            "error": str(e)
        })
        print(f"  Result: ERROR - {str(e)}")

with open("test_results_summary.json", "w") as f:
    json.dump(results, f, indent=2)

print("Finished running all tests. Results saved to test_results_summary.json")
