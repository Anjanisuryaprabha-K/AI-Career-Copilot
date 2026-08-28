from typing import Dict, Any, List

class RoadmapService:
    @staticmethod
    def get_supported_tracks() -> List[Dict[str, str]]:
        return [
            {"track_id": "dsa", "title": "Data Structures & Algorithms (DSA)", "category": "Problem Solving", "difficulty": "Intermediate", "icon": "💻"},
            {"track_id": "mern", "title": "MERN Stack Web Development", "category": "Full Stack", "difficulty": "Intermediate", "icon": "⚛️"},
            {"track_id": "java_fullstack", "title": "Java Full Stack & Spring Boot", "category": "Enterprise Full Stack", "difficulty": "Intermediate", "icon": "☕"},
            {"track_id": "backend", "title": "Backend Engineering & FastAPI", "category": "Backend", "difficulty": "Advanced", "icon": "⚙️"},
            {"track_id": "system_design", "title": "System Design (HLD & LLD)", "category": "Architecture", "difficulty": "Advanced", "icon": "📐"},
            {"track_id": "sql_db", "title": "SQL & Database Management", "category": "Data Engineering", "difficulty": "Beginner to Intermediate", "icon": "🗄️"},
            {"track_id": "cs_fundamentals", "title": "Core CS Fundamentals (OS, DBMS, CN)", "category": "Core CS", "difficulty": "Beginner to Intermediate", "icon": "📚"}
        ]

    @staticmethod
    def get_track_roadmap(track_id: str) -> Dict[str, Any]:
        tracks = {
            "dsa": {
                "track_id": "dsa",
                "title": "Data Structures & Algorithms (Placement Mastery)",
                "category": "Problem Solving",
                "difficulty": "Intermediate",
                "total_weeks": 4,
                "weeks": [
                    {
                        "week_number": 1,
                        "week_title": "Arrays, Two Pointers & Hashing",
                        "learning_objectives": ["Master O(1) hash table lookups", "Apply two pointer techniques for sorted arrays", "Understand sliding window boundaries"],
                        "videos": [
                            {"video_id": "dsa_w1_v1", "title": "Arrays & Dynamic Memory Allocation in Depth", "channel": "Striver (take U forward)", "concept": "Arrays", "duration": "28 mins", "youtube_url": "https://www.youtube.com/watch?v=37E9ckMDdTk", "practice_link": "https://leetcode.com/problems/two-sum/"},
                            {"video_id": "dsa_w1_v2", "title": "Two Pointer Technique - Two Sum II & 3Sum", "channel": "NeetCode", "concept": "Two Pointers", "duration": "22 mins", "youtube_url": "https://www.youtube.com/watch?v=cQ1Oz4ckceM", "practice_link": "https://leetcode.com/problems/3sum/"},
                            {"video_id": "dsa_w1_v3", "title": "Sliding Window Maximum & Fixed Window Pattern", "channel": "Abdul Bari", "concept": "Sliding Window", "duration": "35 mins", "youtube_url": "https://www.youtube.com/watch?v=DfljaUwZsXg", "practice_link": "https://leetcode.com/problems/sliding-window-maximum/"},
                            {"video_id": "dsa_w1_v4", "title": "Prefix Sum & Subarray Sum Equals K", "channel": "Kevin Naughton Jr.", "concept": "Prefix Sum", "duration": "18 mins", "youtube_url": "https://www.youtube.com/watch?v=fFVZt-6sgyo", "practice_link": "https://leetcode.com/problems/subarray-sum-equals-k/"},
                            {"video_id": "dsa_w1_v5", "title": "Kadane's Algorithm - Maximum Subarray", "channel": "Nick White", "concept": "Kadane Algo", "duration": "15 mins", "youtube_url": "https://www.youtube.com/watch?v=5WZl3MMT0Eg", "practice_link": "https://leetcode.com/problems/maximum-subarray/"},
                            {"video_id": "dsa_w1_v6", "title": "Dutch National Flag Algorithm (Sort 0s, 1s, 2s)", "channel": "Striver", "concept": "Sorting", "duration": "20 mins", "youtube_url": "https://www.youtube.com/watch?v=tp8JIuCXBaU", "practice_link": "https://leetcode.com/problems/sort-colors/"},
                            {"video_id": "dsa_w1_v7", "title": "Container With Most Water - Optimal Proof", "channel": "NeetCode", "concept": "Two Pointers", "duration": "16 mins", "youtube_url": "https://www.youtube.com/watch?v=UuiTKBwPgAo", "practice_link": "https://leetcode.com/problems/container-with-most-water/"},
                            {"video_id": "dsa_w1_v8", "title": "Trapping Rain Water - 2 Pointers vs Monotonic Stack", "channel": "Tech Dose", "concept": "Two Pointers", "duration": "24 mins", "youtube_url": "https://www.youtube.com/watch?v=ZI2z5pq0TqA", "practice_link": "https://leetcode.com/problems/trapping-rain-water/"},
                            {"video_id": "dsa_w1_v9", "title": "Longest Consecutive Sequence in O(N)", "channel": "Striver", "concept": "Hashing", "duration": "25 mins", "youtube_url": "https://www.youtube.com/watch?v=qgizvmgeyUM", "practice_link": "https://leetcode.com/problems/longest-consecutive-sequence/"},
                            {"video_id": "dsa_w1_v10", "title": "4Sum Problem & Generalizing K-Sum", "channel": "NeetCode", "concept": "Hashing", "duration": "30 mins", "youtube_url": "https://www.youtube.com/watch?v=EYeR-_1NRlQ", "practice_link": "https://leetcode.com/problems/4sum/"}
                        ]
                    }
                ]
            },
            "mern": {
                "track_id": "mern",
                "title": "MERN Stack Web Development (React, Node, MongoDB)",
                "category": "Full Stack",
                "difficulty": "Intermediate",
                "total_weeks": 4,
                "weeks": [
                    {
                        "week_number": 1,
                        "week_title": "React 18 Architecture, Hooks & Tailwind CSS",
                        "learning_objectives": ["Understand Virtual DOM diffing", "Master useEffect, useMemo, useCallback", "Build responsive layouts with Tailwind CSS"],
                        "videos": [
                            {"video_id": "mern_w1_v1", "title": "React 18 Complete Course for Beginners", "channel": "Traversy Media", "concept": "React Basics", "duration": "45 mins", "youtube_url": "https://www.youtube.com/watch?v=w7ejDZ8SWv8", "practice_link": "https://react.dev/learn"},
                            {"video_id": "mern_w1_v2", "title": "Mastering React Hooks (useState, useEffect, useRef)", "channel": "Web Dev Simplified", "concept": "React Hooks", "duration": "30 mins", "youtube_url": "https://www.youtube.com/watch?v=TNhaISOUy6Q", "practice_link": "https://react.dev/reference/react/hooks"}
                        ]
                    }
                ]
            }
        }
        if track_id not in tracks:
            return tracks["dsa"]
        return tracks[track_id]
