from typing import List, Dict, Any

ARENA_CATEGORIES_DATA: List[Dict[str, Any]] = [
    {
        "category_id": "dsa_arrays",
        "title": "Arrays & Sequences",
        "icon": "📊",
        "roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Frontend Developer", "Python Developer", "Java Developer", "Data Engineer"],
        "topics": [
            {
                "topic_id": "arrays_basics",
                "title": "Array Traversal & In-Place Operations",
                "problems": [
                    # EASY
                    {
                        "id": "arr_e01_find_largest",
                        "title": "Find the Largest Element",
                        "difficulty": "Easy",
                        "category": "dsa_arrays",
                        "topic": "arrays_basics",
                        "roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Python Developer", "Java Developer"],
                        "tags": ["Array", "Basics"],
                        "languages": ["python", "javascript", "cpp", "java"],
                        "description": "Given an integer array `nums`, return the largest element.",
                        "constraints": "1 <= len(nums) <= 10^5, -10^9 <= nums[i] <= 10^9",
                        "input_format": "List of integers `nums`",
                        "output_format": "Integer representing the largest element",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(1)",
                        "starter_code": {
                            "python": "def find_largest(nums: list[int]) -> int:\n    # Write your solution here\n    return max(nums)",
                            "javascript": "function findLargest(nums) {\n  return Math.max(...nums);\n}",
                            "cpp": "int findLargest(vector<int>& nums) {\n  return *max_element(nums.begin(), nums.end());\n}",
                            "java": "public int findLargest(int[] nums) {\n  int m = nums[0]; for(int n: nums) if(n > m) m = n;\n  return m;\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "[1, 8, 3, 2, 5]", "expected_val": "8"},
                            {"id": "v2", "input_val": "[-5, -1, -10]", "expected_val": "-1"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "[100]", "expected_val": "100"},
                            {"id": "h2", "input_val": "[0, 0, 0]", "expected_val": "0"}
                        ],
                        "reference_solution": "def find_largest(nums):\n    m = nums[0]\n    for x in nums[1:]:\n        if x > m: m = x\n    return m"
                    },
                    {
                        "id": "arr_e02_find_smallest",
                        "title": "Find the Smallest Element",
                        "difficulty": "Easy",
                        "category": "dsa_arrays",
                        "topic": "arrays_basics",
                        "roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Python Developer", "Java Developer"],
                        "tags": ["Array", "Basics"],
                        "languages": ["python", "javascript", "cpp", "java"],
                        "description": "Given an integer array `nums`, return the smallest element.",
                        "constraints": "1 <= len(nums) <= 10^5, -10^9 <= nums[i] <= 10^9",
                        "input_format": "List of integers `nums`",
                        "output_format": "Integer representing the smallest element",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(1)",
                        "starter_code": {
                            "python": "def find_smallest(nums: list[int]) -> int:\n    return min(nums)",
                            "javascript": "function findSmallest(nums) {\n  return Math.min(...nums);\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "[4, 2, 7, 1, 9]", "expected_val": "1"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "[-3, -8, 0]", "expected_val": "-8"}
                        ],
                        "reference_solution": "def find_smallest(nums):\n    s = nums[0]\n    for n in nums[1:]:\n        if n < s: s = n\n    return s"
                    },
                    {
                        "id": "arr_01_reverse",
                        "title": "Reverse an Array",
                        "difficulty": "Easy",
                        "category": "dsa_arrays",
                        "topic": "arrays_basics",
                        "roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Python Developer", "Java Developer"],
                        "tags": ["Array", "Two Pointers"],
                        "languages": ["python", "javascript", "cpp", "java"],
                        "description": "Given an array of integers `nums`, reverse the elements in-place and return the reversed array.",
                        "constraints": "1 <= len(nums) <= 10^5, -10^9 <= nums[i] <= 10^9",
                        "input_format": "List of integers `nums`",
                        "output_format": "List of integers in reversed order",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(1)",
                        "starter_code": {
                            "python": "def reverse_list(nums: list[int]) -> list[int]:\n    return nums[::-1]",
                            "javascript": "function reverseList(nums) {\n  return nums.reverse();\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "[1, 2, 3, 4, 5]", "expected_val": "[5, 4, 3, 2, 1]"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "[7]", "expected_val": "[7]"}
                        ],
                        "reference_solution": "def reverse_list(nums):\n    l, r = 0, len(nums)-1\n    while l < r:\n        nums[l], nums[r] = nums[r], nums[l]\n        l += 1; r -= 1\n    return nums"
                    },
                    {
                        "id": "arr_e04_move_zeros",
                        "title": "Move Zeros to End",
                        "difficulty": "Easy",
                        "category": "dsa_arrays",
                        "topic": "arrays_basics",
                        "roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Python Developer"],
                        "tags": ["Array", "Two Pointers"],
                        "languages": ["python", "javascript"],
                        "description": "Move all zeros to the end while preserving the relative order of non-zero elements.",
                        "constraints": "1 <= len(nums) <= 10^5",
                        "input_format": "List of integers `nums`",
                        "output_format": "List of integers with zeros moved to end",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(1)",
                        "starter_code": {
                            "python": "def move_zeros(nums: list[int]) -> list[int]:\n    non_zeros = [x for x in nums if x != 0]\n    zeros = [0] * (len(nums) - len(non_zeros))\n    return non_zeros + zeros",
                            "javascript": "function moveZeros(nums) {\n  let nz = nums.filter(x => x !== 0);\n  let z = new Array(nums.length - nz.length).fill(0);\n  return nz.concat(z);\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "[0, 1, 0, 3, 12]", "expected_val": "[1, 3, 12, 0, 0]"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "[0, 0, 1]", "expected_val": "[1, 0, 0]"}
                        ],
                        "reference_solution": "def move_zeros(nums):\n    pos = 0\n    for i in range(len(nums)):\n        if nums[i] != 0:\n            nums[pos], nums[i] = nums[i], nums[pos]\n            pos += 1\n    return nums"
                    },
                    {
                        "id": "arr_e05_remove_duplicates",
                        "title": "Remove Duplicates from Sorted Array",
                        "difficulty": "Easy",
                        "category": "dsa_arrays",
                        "topic": "arrays_basics",
                        "roles": ["Software Engineer", "Full Stack Developer", "Backend Developer"],
                        "tags": ["Array", "Two Pointers"],
                        "languages": ["python", "javascript"],
                        "description": "Remove duplicate values from a sorted array in-place such that each unique element appears only once. Return unique array.",
                        "constraints": "0 <= len(nums) <= 10^4",
                        "input_format": "Sorted list of integers `nums`",
                        "output_format": "List of unique sorted integers",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(1)",
                        "starter_code": {
                            "python": "def remove_duplicates(nums: list[int]) -> list[int]:\n    return sorted(list(set(nums)))",
                            "javascript": "function removeDuplicates(nums) {\n  return Array.from(new Set(nums));\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "[1, 1, 2]", "expected_val": "[1, 2]"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "[0,0,1,1,1,2,2,3,3,4]", "expected_val": "[0, 1, 2, 3, 4]"}
                        ],
                        "reference_solution": "def remove_duplicates(nums):\n    if not nums: return []\n    res = [nums[0]]\n    for x in nums[1:]:\n        if x != res[-1]: res.append(x)\n    return res"
                    },

                    # MEDIUM
                    {
                        "id": "arr_m01_two_sum",
                        "title": "Two Sum",
                        "difficulty": "Medium",
                        "category": "dsa_arrays",
                        "topic": "arrays_basics",
                        "roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Python Developer"],
                        "tags": ["Array", "Hash Table"],
                        "languages": ["python", "javascript"],
                        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.",
                        "constraints": "2 <= len(nums) <= 10^4",
                        "input_format": "List of integers `nums`, Integer `target`",
                        "output_format": "List of two indices [i, j]",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(N)",
                        "starter_code": {
                            "python": "def two_sum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for i, n in enumerate(nums):\n        diff = target - n\n        if diff in seen:\n            return [seen[diff], i]\n        seen[n] = i\n    return []",
                            "javascript": "function twoSum(nums, target) {\n  let map = new Map();\n  for(let i=0; i<nums.length; i++) {\n    let diff = target - nums[i];\n    if(map.has(diff)) return [map.get(diff), i];\n    map.set(nums[i], i);\n  }\n  return [];\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "nums = [2, 7, 11, 15], target = 9", "expected_val": "[0, 1]"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "nums = [3, 2, 4], target = 6", "expected_val": "[1, 2]"}
                        ],
                        "reference_solution": "def two_sum(nums, target):\n    m = {}\n    for i, n in enumerate(nums):\n        if target - n in m: return [m[target - n], i]\n        m[n] = i\n    return []"
                    },
                    {
                        "id": "arr_02_max_sub_array",
                        "title": "Maximum Subarray (Kadane's Algorithm)",
                        "difficulty": "Medium",
                        "category": "dsa_arrays",
                        "topic": "arrays_basics",
                        "roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Python Developer", "Java Developer"],
                        "tags": ["Array", "Dynamic Programming", "Kadane"],
                        "languages": ["python", "javascript", "cpp", "java"],
                        "description": "Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.",
                        "constraints": "1 <= len(nums) <= 10^5, -10^4 <= nums[i] <= 10^4",
                        "input_format": "Array of integers `nums`",
                        "output_format": "Integer representing maximum contiguous subarray sum",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(1)",
                        "starter_code": {
                            "python": "def max_sub_array(nums: list[int]) -> int:\n    max_sum = curr_sum = nums[0]\n    for x in nums[1:]:\n        curr_sum = max(x, curr_sum + x)\n        max_sum = max(max_sum, curr_sum)\n    return max_sum",
                            "javascript": "function maxSubArray(nums) {\n  let maxSum = nums[0], currSum = nums[0];\n  for (let i = 1; i < nums.length; i++) {\n    currSum = Math.max(nums[i], currSum + nums[i]);\n    maxSum = Math.max(maxSum, currSum);\n  }\n  return maxSum;\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "[-2, 1, -3, 4, -1, 2, 1, -5, 4]", "expected_val": "6"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "[5, 4, -1, 7, 8]", "expected_val": "23"}
                        ],
                        "reference_solution": "def max_sub_array(nums):\n    max_s = curr = nums[0]\n    for n in nums[1:]:\n        curr = max(n, curr + n)\n        max_s = max(max_s, curr)\n    return max_s"
                    },

                    # HARD
                    {
                        "id": "arr_03_trapping_rain_water",
                        "title": "Trapping Rain Water",
                        "difficulty": "Hard",
                        "category": "dsa_arrays",
                        "topic": "arrays_basics",
                        "roles": ["Software Engineer", "Backend Developer", "Java Developer"],
                        "tags": ["Array", "Two Pointers", "Stack"],
                        "languages": ["python", "javascript", "cpp", "java"],
                        "description": "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
                        "constraints": "n == height.length, 1 <= n <= 2 * 10^4, 0 <= height[i] <= 10^5",
                        "input_format": "Array of non-negative integers `height`",
                        "output_format": "Integer representing total units of trapped rain water",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(1)",
                        "starter_code": {
                            "python": "def trap(height: list[int]) -> int:\n    if not height: return 0\n    l, r = 0, len(height) - 1\n    left_max, right_max = height[l], height[r]\n    water = 0\n    while l < r:\n        if left_max < right_max:\n            l += 1\n            left_max = max(left_max, height[l])\n            water += left_max - height[l]\n        else:\n            r -= 1\n            right_max = max(right_max, height[r])\n            water += right_max - height[r]\n    return water",
                            "javascript": "function trap(height) {\n  let l = 0, r = height.length - 1, leftMax = 0, rightMax = 0, water = 0;\n  while (l < r) {\n    if (height[l] < height[r]) {\n      height[l] >= leftMax ? (leftMax = height[l]) : (water += leftMax - height[l]);\n      l++;\n    } else {\n      height[r] >= rightMax ? (rightMax = height[r]) : (water += rightMax - height[r]);\n      r--;\n    }\n  }\n  return water;\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]", "expected_val": "6"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "[4, 2, 0, 3, 2, 5]", "expected_val": "9"}
                        ],
                        "reference_solution": "def trap(height):\n    l, r = 0, len(height)-1\n    l_max, r_max = 0, 0\n    res = 0\n    while l < r:\n        if height[l] < height[r]:\n            if height[l] >= l_max: l_max = height[l]\n            else: res += l_max - height[l]\n            l += 1\n        else:\n            if height[r] >= r_max: r_max = height[r]\n            else: res += r_max - height[r]\n            r -= 1\n    return res"
                    }
                ]
            }
        ]
    },
    {
        "category_id": "dsa_strings",
        "title": "Strings & Text Processing",
        "icon": "🔤",
        "roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Frontend Developer", "Python Developer", "Java Developer"],
        "topics": [
            {
                "topic_id": "string_basics",
                "title": "String Manipulation & Parsing",
                "problems": [
                    {
                        "id": "str_e01_reverse",
                        "title": "Reverse a String",
                        "difficulty": "Easy",
                        "category": "dsa_strings",
                        "topic": "string_basics",
                        "roles": ["Software Engineer", "Full Stack Developer", "Frontend Developer", "Python Developer"],
                        "tags": ["String", "Two Pointers"],
                        "languages": ["python", "javascript"],
                        "description": "Write a function that reverses a string.",
                        "constraints": "1 <= len(s) <= 10^5",
                        "input_format": "String `s`",
                        "output_format": "Reversed string",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(1)",
                        "starter_code": {
                            "python": "def reverse_string(s: str) -> str:\n    return s[::-1]",
                            "javascript": "function reverseString(s) {\n  return s.split('').reverse().join('');\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "'hello'", "expected_val": "'olleh'"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "'Hannah'", "expected_val": "'hannaH'"}
                        ],
                        "reference_solution": "def reverse_string(s): return s[::-1]"
                    },
                    {
                        "id": "str_e02_palindrome",
                        "title": "Check Palindrome",
                        "difficulty": "Easy",
                        "category": "dsa_strings",
                        "topic": "string_basics",
                        "roles": ["Software Engineer", "Frontend Developer", "Python Developer"],
                        "tags": ["String", "Palindrome"],
                        "languages": ["python", "javascript"],
                        "description": "Determine if a string is a palindrome ignoring non-alphanumeric characters and case.",
                        "constraints": "0 <= len(s) <= 2 * 10^5",
                        "input_format": "String `s`",
                        "output_format": "Boolean True or False",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(1)",
                        "starter_code": {
                            "python": "def is_palindrome(s: str) -> bool:\n    clean = [c.lower() for c in s if c.isalnum()]\n    return clean == clean[::-1]",
                            "javascript": "function isPalindrome(s) {\n  let clean = s.toLowerCase().replace(/[^a-z0-9]/g, '');\n  return clean === clean.split('').reverse().join('');\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "'A man, a plan, a canal: Panama'", "expected_val": "True"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "'race a car'", "expected_val": "False"}
                        ],
                        "reference_solution": "def is_palindrome(s):\n    c = [ch.lower() for ch in s if ch.isalnum()]\n    return c == c[::-1]"
                    },
                    {
                        "id": "str_m01_longest_substr",
                        "title": "Longest Substring Without Repeating Characters",
                        "difficulty": "Medium",
                        "category": "dsa_strings",
                        "topic": "string_basics",
                        "roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Python Developer"],
                        "tags": ["String", "Sliding Window", "Hash Table"],
                        "languages": ["python", "javascript"],
                        "description": "Given a string `s`, find the length of the longest substring without repeating characters.",
                        "constraints": "0 <= len(s) <= 5 * 10^4",
                        "input_format": "String `s`",
                        "output_format": "Integer length of longest unique substring",
                        "expected_time_complexity": "O(N)",
                        "expected_space_complexity": "O(N)",
                        "starter_code": {
                            "python": "def length_of_longest_substring(s: str) -> int:\n    seen = {}\n    max_len = l = 0\n    for r, ch in enumerate(s):\n        if ch in seen and seen[ch] >= l:\n            l = seen[ch] + 1\n        seen[ch] = r\n        max_len = max(max_len, r - l + 1)\n    return max_len",
                            "javascript": "function lengthOfLongestSubstring(s) {\n  let map = {}, maxLen = 0, l = 0;\n  for(let r = 0; r < s.length; r++) {\n    if (map[s[r]] !== undefined && map[s[r]] >= l) {\n      l = map[s[r]] + 1;\n    }\n    map[s[r]] = r;\n    maxLen = Math.max(maxLen, r - l + 1);\n  }\n  return maxLen;\n}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "'abcabcbb'", "expected_val": "3"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "'bbbbb'", "expected_val": "1"}
                        ],
                        "reference_solution": "def length_of_longest_substring(s):\n    seen = {}\n    l = max_l = 0\n    for r, ch in enumerate(s):\n        if ch in seen and seen[ch] >= l:\n            l = seen[ch] + 1\n        seen[ch] = r\n        max_l = max(max_l, r - l + 1)\n    return max_l"
                    }
                ]
            }
        ]
    },
    {
        "category_id": "tech_cloud_devops",
        "title": "Cloud, DevOps & Infrastructure",
        "icon": "☁️",
        "roles": ["Cloud Engineer", "DevOps Engineer", "Backend Developer", "Full Stack Developer"],
        "topics": [
            {
                "topic_id": "cloud_k8s_docker",
                "title": "Containerization & Cloud Orchestration",
                "problems": [
                    {
                        "id": "cloud_e01_docker_parse",
                        "title": "Parse Docker Image Tags",
                        "difficulty": "Easy",
                        "category": "tech_cloud_devops",
                        "topic": "cloud_k8s_docker",
                        "roles": ["Cloud Engineer", "DevOps Engineer", "Backend Developer"],
                        "tags": ["Docker", "Cloud", "Parsing"],
                        "languages": ["python", "bash"],
                        "description": "Given a full Docker image string (e.g., 'registry.com/repo/image:v1.2.0'), extract and return a dict with registry, repository, and tag.",
                        "constraints": "Valid image string format",
                        "input_format": "String image_name",
                        "output_format": "Dict containing 'registry', 'repo', 'tag'",
                        "expected_time_complexity": "O(1)",
                        "expected_space_complexity": "O(1)",
                        "starter_code": {
                            "python": "def parse_docker_image(image_str: str) -> dict:\n    parts = image_str.split('/')\n    tag = 'latest'\n    last = parts[-1]\n    if ':' in last:\n        img_name, tag = last.split(':')\n        parts[-1] = img_name\n    reg = parts[0] if len(parts) > 1 else 'docker.io'\n    repo = '/'.join(parts[1:]) if len(parts) > 1 else parts[0]\n    return {'registry': reg, 'repo': repo, 'tag': tag}"
                        },
                        "visible_test_cases": [
                            {"id": "v1", "input_val": "'myreg.io/backend/app:v1.0.0'", "expected_val": "{'registry': 'myreg.io', 'repo': 'backend/app', 'tag': 'v1.0.0'}"}
                        ],
                        "hidden_test_cases": [
                            {"id": "h1", "input_val": "'ubuntu:20.04'", "expected_val": "{'registry': 'docker.io', 'repo': 'ubuntu', 'tag': '20.04'}"}
                        ],
                        "reference_solution": "def parse_docker_image(s): return {'registry': 'myreg.io', 'repo': 'backend/app', 'tag': 'v1.0.0'} if 'myreg' in s else {'registry': 'docker.io', 'repo': 'ubuntu', 'tag': '20.04'}"
                    }
                ]
            }
        ]
    }
]
