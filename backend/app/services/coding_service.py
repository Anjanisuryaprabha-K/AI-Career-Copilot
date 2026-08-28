from typing import Dict, Any, List

SAMPLE_PROBLEMS = [
    {
        "id": "potd-1",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "Medium",
        "category": "Sliding Window / Hash Table",
        "acceptance": "64.2%",
        "description": "Given a string `s`, find the length of the longest substring without duplicate characters.",
        "starter_code": {
            "javascript": "function lengthOfLongestSubstring(s) {\n  let set = new Set();\n  let left = 0, maxLen = 0;\n  for (let right = 0; right < s.length; right++) {\n    while (set.has(s[right])) {\n      set.delete(s[left]);\n      left++;\n    }\n    set.add(s[right]);\n    maxLen = Math.max(maxLen, right - left + 1);\n  }\n  return maxLen;\n}",
            "python": "def lengthOfLongestSubstring(s: str) -> int:\n    char_set = set()\n    left = 0\n    max_len = 0\n    for right in range(len(s)):\n        while s[right] in char_set:\n            char_set.remove(s[left])\n            left += 1\n        char_set.add(s[right])\n        max_len = max(max_len, right - left + 1)\n    return max_len"
        },
        "test_cases": [
            {"input": "abcabcbb", "expected": 3},
            {"input": "bbbbb", "expected": 1},
            {"input": "pwwkew", "expected": 3}
        ]
    },
    {
        "id": "p-2",
        "title": "Two Sum",
        "difficulty": "Easy",
        "category": "Hash Table",
        "acceptance": "82.4%",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.",
        "starter_code": {
            "javascript": "function twoSum(nums, target) {\n  const map = new Map();\n  for (let i = 0; i < nums.length; i++) {\n    const comp = target - nums[i];\n    if (map.has(comp)) return [map.get(comp), i];\n    map.set(nums[i], i);\n  }\n  return [];\n}",
            "python": "def twoSum(nums: list[int], target: int) -> list[int]:\n    lookup = {}\n    for i, num in enumerate(nums):\n        comp = target - num\n        if comp in lookup:\n            return [lookup[comp], i]\n        lookup[num] = i\n    return []"
        },
        "test_cases": [
            {"input": "[2,7,11,15], target=9", "expected": "[0, 1]"},
            {"input": "[3,2,4], target=6", "expected": "[1, 2]"}
        ]
    }
]

class CodingService:
    @staticmethod
    def get_all_problems() -> List[Dict[str, Any]]:
        return SAMPLE_PROBLEMS

    @staticmethod
    def get_problem_by_id(pid: str) -> Dict[str, Any]:
        for p in SAMPLE_PROBLEMS:
            if p["id"] == pid:
                return p
        return SAMPLE_PROBLEMS[0]

    @staticmethod
    def run_code(code: str, language: str, problem_id: str) -> Dict[str, Any]:
        # Simulated instant test case execution
        return {
            "status": "Accepted",
            "passed_tests": 3,
            "total_tests": 3,
            "runtime_ms": 58,
            "memory_mb": 14.2,
            "test_results": [
                {"test_id": 1, "passed": True, "input": "abcabcbb", "output": 3, "expected": 3},
                {"test_id": 2, "passed": True, "input": "bbbbb", "output": 1, "expected": 1},
                {"test_id": 3, "passed": True, "input": "pwwkew", "output": 3, "expected": 3}
            ]
        }
