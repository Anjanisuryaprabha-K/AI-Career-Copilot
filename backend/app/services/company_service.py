class CompanyService:
    COMPANIES = [
        {
            "id": "amazon",
            "name": "Amazon",
            "logo": "📦",
            "tier": "FAANG / Big Tech",
            "avg_ctc": "₹18 - 28 LPA",
            "difficulty": "Hard",
            "rounds_breakdown": [
                {"round": 1, "name": "Online Assessment (OA)", "type": "2 Coding + Work Style Assessment", "duration": "90 mins"},
                {"round": 2, "name": "Technical Round 1", "type": "Data Structures (Trees, Graphs, DP)", "duration": "60 mins"},
                {"round": 3, "name": "Technical Round 2", "type": "System Design / LLD + Coding", "duration": "60 mins"},
                {"round": 4, "name": "Bar Raiser / LP", "type": "Leadership Principles (STAR Method)", "duration": "60 mins"}
            ],
            "top_topics": ["Binary Trees", "Graphs (BFS/DFS)", "Dynamic Programming", "Priority Queues", "Amazon Leadership Principles"],
            "frequent_questions": [
                "Find Median from Data Stream",
                "Course Schedule (Topological Sort)",
                "Word Ladder",
                "LRU Cache Design",
                "Tell me about a time you had to make a decision under ambiguity."
            ]
        },
        {
            "id": "google",
            "name": "Google",
            "logo": "🔍",
            "tier": "FAANG / Big Tech",
            "avg_ctc": "₹22 - 35 LPA",
            "difficulty": "Very Hard",
            "rounds_breakdown": [
                {"round": 1, "name": "Online Coding Challenge", "type": "2 Algorithmic Problems", "duration": "90 mins"},
                {"round": 2, "name": "Technical Interview 1", "type": "Advanced DSA & Graphs", "duration": "45 mins"},
                {"round": 3, "name": "Technical Interview 2", "type": "DP & Optimization", "duration": "45 mins"},
                {"round": 4, "name": "Googleyness & Leadership", "type": "Behavioral & Culture Fit", "duration": "45 mins"}
            ],
            "top_topics": ["Graph Algorithms", "Trie / String Matching", "Bit Manipulation", "Segment Trees", "Clean Code"],
            "frequent_questions": [
                "Longest Valid Parentheses",
                "Alien Dictionary",
                "Evaluate Division",
                "Serialize and Deserialize Binary Tree"
            ]
        },
        {
            "id": "swiggy",
            "name": "Swiggy",
            "logo": "🛵",
            "tier": "Top Tech Unicorn",
            "avg_ctc": "₹14 - 22 LPA",
            "difficulty": "Medium - Hard",
            "rounds_breakdown": [
                {"round": 1, "name": "HackerRank OA", "type": "3 Coding Problems", "duration": "75 mins"},
                {"round": 2, "name": "Machine Coding Round", "type": "Live LLD / Schema & API Design", "duration": "90 mins"},
                {"round": 3, "name": "Problem Solving & DSA", "type": "Hash Maps, Slidng Window, Heap", "duration": "60 mins"},
                {"round": 4, "name": "Techno-Managerial", "type": "Past Projects & Scalability", "duration": "45 mins"}
            ],
            "top_topics": ["LLD / Object Oriented Design", "Sliding Window", "Redis Caching", "REST APIs", "Concurrency"],
            "frequent_questions": [
                "Design a Delivery Driver Matching System",
                "Subarray Sum Equals K",
                "Sliding Window Maximum"
            ]
        },
        {
            "id": "razorpay",
            "name": "Razorpay",
            "logo": "💳",
            "tier": "FinTech Unicorn",
            "avg_ctc": "₹15 - 24 LPA",
            "difficulty": "Hard",
            "rounds_breakdown": [
                {"round": 1, "name": "Coding Test", "type": "2 Problems (DSA)", "duration": "60 mins"},
                {"round": 2, "name": "DSA & Problem Solving", "type": "Arrays, Trees, DP", "duration": "60 mins"},
                {"round": 3, "name": "System Design / Backend", "type": "Database Indexing, Transactions, Kafka", "duration": "60 mins"},
                {"round": 4, "name": "Culture Fit", "type": "Ownership & Problem Solving Mindset", "duration": "45 mins"}
            ],
            "top_topics": ["Transactions & Idempotency", "Concurrency", "Dynamic Programming", "Trees & Heaps"],
            "frequent_questions": [
                "Design an Idempotent Payment Gateway",
                "Trapping Rain Water",
                "Coin Change"
            ]
        }
    ]

    @classmethod
    def get_all_companies(cls):
        return cls.COMPANIES

    @classmethod
    def get_company_by_id(cls, comp_id: str):
        for c in cls.COMPANIES:
            if c["id"].lower() == comp_id.lower():
                return c
        return cls.COMPANIES[0]
