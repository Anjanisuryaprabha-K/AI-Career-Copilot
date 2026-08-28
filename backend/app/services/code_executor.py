import os
import sys
import time
import uuid
import shutil
import tempfile
import subprocess
import json
import re
from typing import Dict, Any, List, Optional

MAX_OUTPUT_BYTES = 1_000_000  # 1MB cap on stdout/stderr to prevent memory leaks

class CodeExecutor:

    @classmethod
    def get_sanitized_env(cls, tmpdir: str) -> Dict[str, str]:
        """Provides an isolated environment for execution, stripping application secrets."""
        safe_path = os.environ.get("PATH", "")
        safe_sysroot = os.environ.get("SYSTEMROOT", "")
        safe_windir = os.environ.get("WINDIR", "")
        env = {
            "PATH": safe_path,
            "TEMP": tmpdir,
            "TMP": tmpdir,
        }
        if safe_sysroot:
            env["SYSTEMROOT"] = safe_sysroot
        if safe_windir:
            env["WINDIR"] = safe_windir
        return env

    @classmethod
    def check_language_availability(cls, language: str) -> Optional[Dict[str, str]]:
        """Returns compiler/interpreter command or None if language runtime is unavailable."""
        lang = language.lower().strip()
        if lang in ["python", "python3", "py"]:
            py_bin = sys.executable or shutil.which("python3") or shutil.which("python")
            return {"type": "python", "bin": py_bin} if py_bin else None
        elif lang in ["javascript", "js", "node", "nodejs"]:
            node_bin = shutil.which("node") or shutil.which("nodejs")
            return {"type": "javascript", "bin": node_bin} if node_bin else None
        elif lang in ["cpp", "c++"]:
            cpp_bin = shutil.which("g++") or shutil.which("clang++")
            return {"type": "cpp", "bin": cpp_bin} if cpp_bin else None
        elif lang in ["java"]:
            javac_bin = shutil.which("javac")
            java_bin = shutil.which("java")
            return {"type": "java", "javac": javac_bin, "java": java_bin} if (javac_bin and java_bin) else None
        return None

    @classmethod
    def sanitize_error(cls, error_msg: str, tmpdir: str) -> str:
        """Strips absolute server directory paths and system paths from compiler/runtime outputs."""
        if not error_msg:
            return ""
        clean = error_msg.replace(tmpdir, "").replace(os.path.dirname(tmpdir), "")
        # Remove Windows/Unix absolute paths
        clean = re.sub(r'[A-Za-z]:\\[^:\n\r]+', 'solution', clean)
        clean = re.sub(r'/[^:\n\r]+/solution', 'solution', clean)
        return clean.strip()

    @classmethod
    def compare_outputs(cls, actual: str, expected: str) -> bool:
        """Robust output comparison handling line endings and trailing whitespace."""
        if actual is None or expected is None:
            return False

        a_str = str(actual).replace("\r\n", "\n").strip()
        e_str = str(expected).replace("\r\n", "\n").strip()

        if a_str == e_str:
            return True

        # Compare line-by-line with trailing space stripped
        a_lines = [line.rstrip() for line in a_str.split("\n") if line.rstrip()]
        e_lines = [line.rstrip() for line in e_str.split("\n") if line.rstrip()]

        if a_lines == e_lines:
            return True

        # Try JSON evaluation normalization for array/object representations
        try:
            a_json = json.loads(a_str)
            e_json = json.loads(e_str)
            if a_json == e_json:
                return True
        except Exception:
            pass

        return False

    @classmethod
    def execute_test_case(
        cls,
        code: str,
        language: str,
        input_val: str,
        expected_val: str,
        timeout_seconds: float = 3.0,
        execution_type: str = "function"
    ) -> Dict[str, Any]:
        runtime_info = cls.check_language_availability(language)
        if not runtime_info:
            return {
                "status": "LANGUAGE_UNAVAILABLE",
                "passed": False,
                "input": input_val,
                "expected": expected_val,
                "actual": "Language runtime unavailable",
                "execution_time": 0.0,
                "error": f"Language runtime '{language}' is not configured on the server environment."
            }

        tmpdir = tempfile.mkdtemp(prefix=f"coding_exec_{uuid.uuid4().hex[:8]}_")
        start_time = time.time()
        env = cls.get_sanitized_env(tmpdir)

        try:
            lang_type = runtime_info["type"]
            input_clean = str(input_val).strip()

            # ----------------------------------------------------
            # 1. PYTHON EXECUTION
            # ----------------------------------------------------
            if lang_type == "python":
                script_path = os.path.join(tmpdir, "solution.py")
                encoded_input = json.dumps(input_clean)
                # Wrap python function execution or standard stdin/stdout
                wrapper_code = (
                    f"{code}\n\n"
                    f"if __name__ == '__main__':\n"
                    f"    import sys, json\n"
                    f"    try:\n"
                    f"        input_str = {encoded_input}\n"
                    f"        funcs = [v for k, v in list(globals().items()) if callable(v) and not k.startswith('__') and k != 'CodeExecutor']\n"
                    f"        if funcs:\n"
                    f"            try:\n"
                    f"                if isinstance(input_str, str) and input_str.startswith('[') and input_str.endswith(']'):\n"
                    f"                    args = json.loads(input_str)\n"
                    f"                elif isinstance(input_str, str):\n"
                    f"                    try:\n"
                    f"                        args = json.loads('[' + input_str + ']')\n"
                    f"                    except Exception:\n"
                    f"                        args = [input_str]\n"
                    f"                else:\n"
                    f"                    args = [input_str]\n"
                    f"            except Exception:\n"
                    f"                args = [input_str]\n"
                    f"            try:\n"
                    f"                res = funcs[0](*args)\n"
                    f"            except TypeError:\n"
                    f"                res = funcs[0](args)\n"
                    f"            if res is not None:\n"
                    f"                print(json.dumps(res) if isinstance(res, (list, dict, bool)) else res)\n"
                    f"    except Exception as e:\n"
                    f"        sys.stderr.write(f'{{type(e).__name__}}: {{e}}')\n"
                    f"        sys.exit(1)\n"
                )
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(wrapper_code)

                proc = subprocess.Popen(
                    [runtime_info["bin"], script_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=tmpdir,
                    env=env
                )

                try:
                    stdout, stderr = proc.communicate(input=input_clean, timeout=timeout_seconds)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.communicate()
                    return {
                        "status": "TIME_LIMIT_EXCEEDED",
                        "passed": False,
                        "input": input_val,
                        "expected": expected_val,
                        "actual": "Time Limit Exceeded",
                        "execution_time": round(timeout_seconds, 3),
                        "error": f"Time Limit Exceeded ({int(timeout_seconds * 1000)}ms)"
                    }

                exec_time = round(time.time() - start_time, 3)
                stdout = (stdout or "")[:MAX_OUTPUT_BYTES]
                stderr = (stderr or "")[:MAX_OUTPUT_BYTES]

                if proc.returncode != 0:
                    clean_err = cls.sanitize_error(stderr or stdout, tmpdir)
                    return {
                        "status": "RUNTIME_ERROR",
                        "passed": False,
                        "input": input_val,
                        "expected": expected_val,
                        "actual": "Runtime Error",
                        "execution_time": exec_time,
                        "error": clean_err
                    }

                actual_out = stdout.strip()
                passed = cls.compare_outputs(actual_out, expected_val)

                return {
                    "status": "ACCEPTED" if passed else "WRONG_ANSWER",
                    "passed": passed,
                    "input": input_val,
                    "expected": expected_val,
                    "actual": actual_out,
                    "execution_time": exec_time,
                    "error": None if passed else f"Output mismatch. Expected: {expected_val}, Got: {actual_out}"
                }

            # ----------------------------------------------------
            # 2. JAVASCRIPT EXECUTION
            # ----------------------------------------------------
            elif lang_type == "javascript":
                script_path = os.path.join(tmpdir, "solution.js")
                encoded_input_js = json.dumps(input_clean)
                wrapper_code = (
                    f"{code}\n\n"
                    f"try {{\n"
                    f"  const inputStr = {encoded_input_js};\n"
                    f"  const funcs = Object.keys(global).filter(k => typeof global[k] === 'function');\n"
                    f"  let fn = null;\n"
                    f"  if (typeof reverseList === 'function') fn = reverseList;\n"
                    f"  else if (typeof twoSum === 'function') fn = twoSum;\n"
                    f"  else if (typeof maxSubArray === 'function') fn = maxSubArray;\n"
                    f"  else if (typeof isValid === 'function') fn = isValid;\n"
                    f"  else if (typeof trap === 'function') fn = trap;\n"
                    f"  if (fn) {{\n"
                    f"    let args;\n"
                    f"    try {{ args = JSON.parse('[' + inputStr + ']'); }} catch(e) {{ args = [inputStr]; }}\n"
                    f"    const res = fn(...args);\n"
                    f"    if (res !== undefined) console.log(typeof res === 'object' ? JSON.stringify(res) : res);\n"
                    f"  }}\n"
                    f"}} catch (err) {{\n"
                    f"  console.error(err.message);\n"
                    f"  process.exit(1);\n"
                    f"}}\n"
                )
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(wrapper_code)

                proc = subprocess.Popen(
                    [runtime_info["bin"], script_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=tmpdir,
                    env=env
                )

                try:
                    stdout, stderr = proc.communicate(input=input_clean, timeout=timeout_seconds)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.communicate()
                    return {
                        "status": "TIME_LIMIT_EXCEEDED",
                        "passed": False,
                        "input": input_val,
                        "expected": expected_val,
                        "actual": "Time Limit Exceeded",
                        "execution_time": round(timeout_seconds, 3),
                        "error": f"Time Limit Exceeded ({int(timeout_seconds * 1000)}ms)"
                    }

                exec_time = round(time.time() - start_time, 3)
                if proc.returncode != 0:
                    return {
                        "status": "RUNTIME_ERROR",
                        "passed": False,
                        "input": input_val,
                        "expected": expected_val,
                        "actual": "Runtime Error",
                        "execution_time": exec_time,
                        "error": cls.sanitize_error(stderr, tmpdir)
                    }

                actual_out = stdout.strip()
                passed = cls.compare_outputs(actual_out, expected_val)

                return {
                    "status": "ACCEPTED" if passed else "WRONG_ANSWER",
                    "passed": passed,
                    "input": input_val,
                    "expected": expected_val,
                    "actual": actual_out,
                    "execution_time": exec_time,
                    "error": None if passed else f"Output mismatch. Expected: {expected_val}, Got: {actual_out}"
                }

            # ----------------------------------------------------
            # 3. C++ EXECUTION
            # ----------------------------------------------------
            elif lang_type == "cpp":
                source_path = os.path.join(tmpdir, "solution.cpp")
                binary_path = os.path.join(tmpdir, "solution.exe" if os.name == "nt" else "solution")

                with open(source_path, "w", encoding="utf-8") as f:
                    f.write(code)

                # Compilation step
                compile_proc = subprocess.run(
                    [runtime_info["bin"], "-O2", source_path, "-o", binary_path],
                    capture_output=True,
                    text=True,
                    cwd=tmpdir,
                    env=env,
                    timeout=10.0
                )

                if compile_proc.returncode != 0:
                    clean_compile_err = cls.sanitize_error(compile_proc.stderr, tmpdir)
                    return {
                        "status": "COMPILATION_ERROR",
                        "passed": False,
                        "input": input_val,
                        "expected": expected_val,
                        "actual": "Compilation Error",
                        "execution_time": 0.0,
                        "error": clean_compile_err
                    }

                # Execution step
                proc = subprocess.Popen(
                    [binary_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=tmpdir,
                    env=env
                )

                try:
                    stdout, stderr = proc.communicate(input=input_clean, timeout=timeout_seconds)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.communicate()
                    return {
                        "status": "TIME_LIMIT_EXCEEDED",
                        "passed": False,
                        "input": input_val,
                        "expected": expected_val,
                        "actual": "Time Limit Exceeded",
                        "execution_time": round(timeout_seconds, 3),
                        "error": f"Time Limit Exceeded ({int(timeout_seconds * 1000)}ms)"
                    }

                exec_time = round(time.time() - start_time, 3)
                if proc.returncode != 0:
                    return {
                        "status": "RUNTIME_ERROR",
                        "passed": False,
                        "input": input_val,
                        "expected": expected_val,
                        "actual": "Runtime Error",
                        "execution_time": exec_time,
                        "error": cls.sanitize_error(stderr, tmpdir)
                    }

                actual_out = stdout.strip()
                passed = cls.compare_outputs(actual_out, expected_val)

                return {
                    "status": "ACCEPTED" if passed else "WRONG_ANSWER",
                    "passed": passed,
                    "input": input_val,
                    "expected": expected_val,
                    "actual": actual_out,
                    "execution_time": exec_time,
                    "error": None if passed else f"Output mismatch. Expected: {expected_val}, Got: {actual_out}"
                }

            # ----------------------------------------------------
            # 4. JAVA EXECUTION
            # ----------------------------------------------------
            elif lang_type == "java":
                source_path = os.path.join(tmpdir, "Solution.java")
                with open(source_path, "w", encoding="utf-8") as f:
                    f.write(code)

                compile_proc = subprocess.run(
                    [runtime_info["javac"], source_path],
                    capture_output=True,
                    text=True,
                    cwd=tmpdir,
                    env=env,
                    timeout=10.0
                )

                if compile_proc.returncode != 0:
                    clean_compile_err = cls.sanitize_error(compile_proc.stderr, tmpdir)
                    return {
                        "status": "COMPILATION_ERROR",
                        "passed": False,
                        "input": input_val,
                        "expected": expected_val,
                        "actual": "Compilation Error",
                        "execution_time": 0.0,
                        "error": clean_compile_err
                    }

                proc = subprocess.Popen(
                    [runtime_info["java"], "-cp", tmpdir, "Solution"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=tmpdir,
                    env=env
                )

                try:
                    stdout, stderr = proc.communicate(input=input_clean, timeout=timeout_seconds)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.communicate()
                    return {
                        "status": "TIME_LIMIT_EXCEEDED",
                        "passed": False,
                        "input": input_val,
                        "expected": expected_val,
                        "actual": "Time Limit Exceeded",
                        "execution_time": round(timeout_seconds, 3),
                        "error": f"Time Limit Exceeded ({int(timeout_seconds * 1000)}ms)"
                    }

                exec_time = round(time.time() - start_time, 3)
                if proc.returncode != 0:
                    return {
                        "status": "RUNTIME_ERROR",
                        "passed": False,
                        "input": input_val,
                        "expected": expected_val,
                        "actual": "Runtime Error",
                        "execution_time": exec_time,
                        "error": cls.sanitize_error(stderr, tmpdir)
                    }

                actual_out = stdout.strip()
                passed = cls.compare_outputs(actual_out, expected_val)

                return {
                    "status": "ACCEPTED" if passed else "WRONG_ANSWER",
                    "passed": passed,
                    "input": input_val,
                    "expected": expected_val,
                    "actual": actual_out,
                    "execution_time": exec_time,
                    "error": None if passed else f"Output mismatch. Expected: {expected_val}, Got: {actual_out}"
                }

        except Exception as e:
            return {
                "status": "RUNTIME_ERROR",
                "passed": False,
                "input": input_val,
                "expected": expected_val,
                "actual": "Execution Error",
                "execution_time": round(time.time() - start_time, 3),
                "error": cls.sanitize_error(str(e), tmpdir)
            }
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

    @classmethod
    def evaluate(cls, code: str, language: str, test_cases: List[Dict[str, Any]], timeout_per_test: float = 3.0) -> Dict[str, Any]:
        """Runs code against test case suite and returns standardized execution payload."""
        if not code or not code.strip():
            return {
                "status": "COMPILATION_ERROR",
                "passed_tests": 0,
                "total_tests": len(test_cases) if test_cases else 0,
                "execution_time": 0.0,
                "memory_used": None,
                "compiler_output": "Empty submission: No source code provided.",
                "runtime_output": "",
                "test_details": []
            }

        runtime_info = cls.check_language_availability(language)
        if not runtime_info:
            return {
                "status": "LANGUAGE_UNAVAILABLE",
                "passed_tests": 0,
                "total_tests": len(test_cases) if test_cases else 0,
                "execution_time": 0.0,
                "memory_used": None,
                "compiler_output": f"Language runtime '{language}' is unavailable in server environment.",
                "runtime_output": "",
                "test_details": []
            }

        if not test_cases:
            return {
                "status": "ACCEPTED",
                "passed_tests": 0,
                "total_tests": 0,
                "execution_time": 0.0,
                "memory_used": None,
                "compiler_output": "",
                "runtime_output": "",
                "test_details": []
            }

        total_cnt = len(test_cases)
        results = []
        passed_cnt = 0
        final_verdict = "ACCEPTED"
        total_time = 0.0
        compiler_msg = ""
        runtime_msg = ""

        for tc in test_cases:
            in_val = str(tc.get("input_val", tc.get("input", "")))
            exp_val = str(tc.get("expected_val", tc.get("expected", "")))

            res = cls.execute_test_case(
                code=code,
                language=language,
                input_val=in_val,
                expected_val=exp_val,
                timeout_seconds=timeout_per_test
            )

            results.append(res)
            total_time += res.get("execution_time", 0.0)

            if res["status"] == "COMPILATION_ERROR":
                final_verdict = "COMPILATION_ERROR"
                compiler_msg = res.get("error", "Compilation failed.")
                break
            elif res["status"] == "LANGUAGE_UNAVAILABLE":
                final_verdict = "LANGUAGE_UNAVAILABLE"
                compiler_msg = res.get("error", "Language runtime unavailable.")
                break
            elif res["status"] == "TIME_LIMIT_EXCEEDED":
                if final_verdict == "ACCEPTED":
                    final_verdict = "TIME_LIMIT_EXCEEDED"
            elif res["status"] == "RUNTIME_ERROR":
                if final_verdict in ["ACCEPTED", "WRONG_ANSWER"]:
                    final_verdict = "RUNTIME_ERROR"
                    runtime_msg = res.get("error", "Runtime error occurred.")
            elif res["status"] == "WRONG_ANSWER":
                if final_verdict == "ACCEPTED":
                    final_verdict = "WRONG_ANSWER"

            if res.get("passed"):
                passed_cnt += 1

        return {
            "status": final_verdict,
            "passed_tests": passed_cnt,
            "total_tests": total_cnt,
            "passed_test_cases": f"{passed_cnt}/{total_cnt}",
            "passed_count": passed_cnt,
            "total_count": total_cnt,
            "execution_time": round(total_time, 3),
            "execution_time_ms": round(total_time * 1000),
            "memory_used": None,
            "compiler_output": compiler_msg,
            "runtime_output": runtime_msg,
            "test_details": results
        }
