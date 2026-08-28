from typing import Dict, Any, List, Optional
from datetime import datetime
from app.repositories.resume_repository import resume_repository
from app.repositories.coding_repository import CodingRepository
from app.repositories.interview_repository import InterviewRepository
from app.repositories.learning_repository import learning_repository
from app.repositories.adaptive_roadmap_repository import adaptive_roadmap_repository
from app.services.youtube_resource_service import YouTubeResourceService

coding_repository = CodingRepository()
interview_repository = InterviewRepository()

class AdaptiveRoadmapService:

    SUPPORTED_ROLES = [
        "Software Engineer",
        "Full Stack Developer",
        "Frontend Developer",
        "Backend Developer",
        "Java Developer",
        "Python Developer",
        "Data Engineer",
        "Data Scientist",
        "Machine Learning Engineer",
        "DevOps Engineer",
        "Cloud Engineer"
    ]

    EXPERIENCE_LEVELS = ["Entry Level / Fresh Grad", "Mid Level (2-4 Yrs)", "Senior Level (5+ Yrs)"]
    COMPANY_TYPES = ["MAANG / Tier-1 Product", "Mid-Size Product", "Startup / Service-Based"]
    PREP_TIMEFRAMES = [2, 4, 8, 12]
    SKILL_LEVELS = ["Beginner", "Intermediate", "Advanced"]

    ROLE_CURRICULA = {
        "Software Engineer": [
            {
                "id": "se_arrays_basics",
                "title": "Arrays & Hash Maps Fundamentals",
                "description": "Master array indexing, hash map lookups, frequency counting, and 2-pointer techniques.",
                "category": "Coding Practice",
                "difficulty": "Easy",
                "estimated_time": "3 Hours",
                "prerequisites": [],
                "default_priority": "High",
                "topic_key": "Arrays"
            },
            {
                "id": "se_cs_os_dbms",
                "title": "Core CS: OS, DBMS & Computer Networks",
                "description": "Review process concurrency, virtual memory, SQL indexing, and TCP/IP protocol stack.",
                "category": "CS Fundamentals",
                "difficulty": "Medium",
                "estimated_time": "5 Hours",
                "prerequisites": [],
                "default_priority": "Medium",
                "topic_key": "OS/DBMS"
            },
            {
                "id": "se_graph_basics",
                "title": "Graph Representations & Adjacency Lists",
                "description": "Understand graph data structures, directed/undirected edges, and matrix/list representations.",
                "category": "Learning Modules",
                "difficulty": "Easy",
                "estimated_time": "2 Hours",
                "prerequisites": ["se_arrays_basics"],
                "default_priority": "Medium",
                "topic_key": "Graphs"
            },
            {
                "id": "se_graph_traversal",
                "title": "Graph Traversals: BFS & DFS Patterns",
                "description": "Implement Breadth-First Search and Depth-First Search for connected components and shortest paths.",
                "category": "Coding Practice",
                "difficulty": "Medium",
                "estimated_time": "4 Hours",
                "prerequisites": ["se_graph_basics"],
                "default_priority": "High",
                "topic_key": "Graphs"
            },
            {
                "id": "se_dp_fundamentals",
                "title": "Dynamic Programming: Recursion to Memoization",
                "description": "Master overlapping subproblems, state transitions, and 1D DP tabulation techniques.",
                "category": "Learning Modules",
                "difficulty": "Medium",
                "estimated_time": "4 Hours",
                "prerequisites": ["se_arrays_basics"],
                "default_priority": "High",
                "topic_key": "Dynamic Programming"
            },
            {
                "id": "se_dp_medium_problems",
                "title": "DP Patterns: Knapsack, Subsets & LIS",
                "description": "Solve classic medium DP problems including 0/1 Knapsack, Longest Common Subsequence, and LIS.",
                "category": "Coding Practice",
                "difficulty": "Medium",
                "estimated_time": "6 Hours",
                "prerequisites": ["se_dp_fundamentals"],
                "default_priority": "High",
                "topic_key": "Dynamic Programming"
            },
            {
                "id": "se_sql_mastery",
                "title": "SQL Join Optimizations & Subqueries",
                "description": "Write complex multi-table SQL queries, aggregate window functions, and indexing strategies.",
                "category": "SQL Preparation",
                "difficulty": "Medium",
                "estimated_time": "3 Hours",
                "prerequisites": ["se_cs_os_dbms"],
                "default_priority": "Medium",
                "topic_key": "SQL"
            },
            {
                "id": "se_behavioral_prosody",
                "title": "Behavioral STAR Method & Speech Prosody",
                "description": "Practice structuring scenario answers with high vocal confidence and clear articulation.",
                "category": "Communication Practice",
                "difficulty": "Easy",
                "estimated_time": "2 Hours",
                "prerequisites": [],
                "default_priority": "Medium",
                "topic_key": "Behavioral"
            },
            {
                "id": "se_mock_technical_oa",
                "title": "Timed Mock Online Coding Assessment (OA)",
                "description": "Simulate a live 90-minute technical OA covering algorithms, time complexity, and edge cases.",
                "category": "Mock Interviews",
                "difficulty": "Hard",
                "estimated_time": "2 Hours",
                "prerequisites": ["se_graph_traversal", "se_dp_medium_problems"],
                "default_priority": "High",
                "topic_key": "Mock Assessment"
            }
        ],
        "Full Stack Developer": [
            {
                "id": "fs_js_ts_core",
                "title": "Modern JavaScript ES6+ & TypeScript System",
                "description": "Master async/await, promises, closure scope, and strict TypeScript interface typing.",
                "category": "Learning Modules",
                "difficulty": "Easy",
                "estimated_time": "3 Hours",
                "prerequisites": [],
                "default_priority": "High",
                "topic_key": "JavaScript"
            },
            {
                "id": "fs_react_architecture",
                "title": "React 18 Component Architecture & Custom Hooks",
                "description": "Build modular React UIs with context state, custom hooks, memoization, and Tailwind CSS.",
                "category": "Projects",
                "difficulty": "Medium",
                "estimated_time": "5 Hours",
                "prerequisites": ["fs_js_ts_core"],
                "default_priority": "High",
                "topic_key": "React"
            },
            {
                "id": "fs_backend_fastapi_node",
                "title": "REST API Engineering with FastAPI / Node.js",
                "description": "Design modular route controllers, JWT authentication middleware, and input schema validation.",
                "category": "Learning Modules",
                "difficulty": "Medium",
                "estimated_time": "4 Hours",
                "prerequisites": ["fs_js_ts_core"],
                "default_priority": "High",
                "topic_key": "FastAPI"
            },
            {
                "id": "fs_db_modelling",
                "title": "MongoDB & PostgreSQL Data Modeling",
                "description": "Implement database schemas, index strategies, transactions, and aggregate pipelines.",
                "category": "SQL Preparation",
                "difficulty": "Medium",
                "estimated_time": "4 Hours",
                "prerequisites": ["fs_backend_fastapi_node"],
                "default_priority": "Medium",
                "topic_key": "Database"
            },
            {
                "id": "fs_dsa_web_problems",
                "title": "Web Engineering Coding Challenges",
                "description": "Solve string manipulation, recursive tree views, and event emitter algorithms.",
                "category": "Coding Practice",
                "difficulty": "Medium",
                "estimated_time": "4 Hours",
                "prerequisites": ["fs_js_ts_core"],
                "default_priority": "Medium",
                "topic_key": "Algorithms"
            },
            {
                "id": "fs_system_design_lld",
                "title": "System Design: Microservices & Caching Layer",
                "description": "Design scalable full-stack web applications with Redis caching and pub/sub queues.",
                "category": "Interview Preparation",
                "difficulty": "Hard",
                "estimated_time": "5 Hours",
                "prerequisites": ["fs_backend_fastapi_node", "fs_db_modelling"],
                "default_priority": "High",
                "topic_key": "System Design"
            },
            {
                "id": "fs_fullstack_capstone",
                "title": "Full-Stack Production App Capstone",
                "description": "Deploy a complete authenticated web application with live DB, state, and Docker.",
                "category": "Projects",
                "difficulty": "Hard",
                "estimated_time": "8 Hours",
                "prerequisites": ["fs_react_architecture", "fs_backend_fastapi_node"],
                "default_priority": "High",
                "topic_key": "Full Stack"
            },
            {
                "id": "fs_mock_interview",
                "title": "Full Stack System Architecture Mock Interview",
                "description": "Conduct a live simulated technical round discussing API design, DB tradeoffs, and prosody.",
                "category": "Mock Interviews",
                "difficulty": "Hard",
                "estimated_time": "2 Hours",
                "prerequisites": ["fs_system_design_lld", "fs_fullstack_capstone"],
                "default_priority": "High",
                "topic_key": "Mock Assessment"
            }
        ],
        "Frontend Developer": [
            {
                "id": "fe_js_deep_dive",
                "title": "JavaScript Internals: Event Loop & DOM",
                "description": "Understand call stack, event loop microtasks, DOM manipulation, and performance profiling.",
                "category": "Learning Modules",
                "difficulty": "Easy",
                "estimated_time": "3 Hours",
                "prerequisites": [],
                "default_priority": "High",
                "topic_key": "JavaScript"
            },
            {
                "id": "fe_react_state_mgmt",
                "title": "React Advanced State & Performance",
                "description": "Optimize component re-renders with useMemo, useCallback, Redux/Zustand, and suspense.",
                "category": "Projects",
                "difficulty": "Medium",
                "estimated_time": "5 Hours",
                "prerequisites": ["fe_js_deep_dive"],
                "default_priority": "High",
                "topic_key": "React"
            },
            {
                "id": "fe_css_responsive_design",
                "title": "Modern CSS Grid, Flexbox & Tailwind",
                "description": "Build complex pixel-perfect responsive layouts, animations, and accessible web components.",
                "category": "Learning Modules",
                "difficulty": "Easy",
                "estimated_time": "3 Hours",
                "prerequisites": [],
                "default_priority": "Medium",
                "topic_key": "CSS"
            },
            {
                "id": "fe_coding_challenges",
                "title": "Frontend Machine Coding Challenges",
                "description": "Build autocomplete dropdowns, virtualized lists, and debounced search UI widgets.",
                "category": "Coding Practice",
                "difficulty": "Medium",
                "estimated_time": "5 Hours",
                "prerequisites": ["fe_js_deep_dive", "fe_react_state_mgmt"],
                "default_priority": "High",
                "topic_key": "Frontend Coding"
            },
            {
                "id": "fe_mock_system_design",
                "title": "Frontend Architecture & System Design Round",
                "description": "Design a client-side architecture for a scalable web app like Google Docs or Netflix UI.",
                "category": "Mock Interviews",
                "difficulty": "Hard",
                "estimated_time": "2 Hours",
                "prerequisites": ["fe_coding_challenges"],
                "default_priority": "High",
                "topic_key": "Mock Assessment"
            }
        ],
        "Backend Developer": [
            {
                "id": "be_concurrency_async",
                "title": "Asynchronous Programming & Concurrency",
                "description": "Master event loops, thread pools, async execution, worker queues, and mutex locks.",
                "category": "Learning Modules",
                "difficulty": "Medium",
                "estimated_time": "4 Hours",
                "prerequisites": [],
                "default_priority": "High",
                "topic_key": "Backend Concurrency"
            },
            {
                "id": "be_db_indexing_sql",
                "title": "Database Schema Design & Query Tuning",
                "description": "Master B-Tree indexes, query execution plans, transactions, ACID guarantees, and PostgreSQL/MySQL.",
                "category": "SQL Preparation",
                "difficulty": "Medium",
                "estimated_time": "4 Hours",
                "prerequisites": [],
                "default_priority": "High",
                "topic_key": "SQL"
            },
            {
                "id": "be_dsa_backend_problems",
                "title": "Backend Algorithmic Challenges",
                "description": "Solve rate-limiting algorithms, LRU caches, graph dependencies, and queue structures.",
                "category": "Coding Practice",
                "difficulty": "Hard",
                "estimated_time": "6 Hours",
                "prerequisites": ["be_concurrency_async"],
                "default_priority": "High",
                "topic_key": "Backend Algorithms"
            },
            {
                "id": "be_distributed_systems",
                "title": "High-Availability System Design (HLD)",
                "description": "Architect load balancers, message brokers (Kafka/RabbitMQ), and distributed caching.",
                "category": "Interview Preparation",
                "difficulty": "Hard",
                "estimated_time": "6 Hours",
                "prerequisites": ["be_concurrency_async", "be_db_indexing_sql"],
                "default_priority": "High",
                "topic_key": "System Design"
            },
            {
                "id": "be_mock_technical_interview",
                "title": "Backend Engineering Live Mock Interview",
                "description": "Mock interview covering API security, DB bottleneck diagnosis, and architectural tradeoffs.",
                "category": "Mock Interviews",
                "difficulty": "Hard",
                "estimated_time": "2 Hours",
                "prerequisites": ["be_dsa_backend_problems", "be_distributed_systems"],
                "default_priority": "High",
                "topic_key": "Mock Assessment"
            }
        ]
    }

    @classmethod
    def get_role_template(cls, role: str) -> List[Dict[str, Any]]:
        # Fallback to Software Engineer if specific role template not defined
        for key in cls.ROLE_CURRICULA:
            if key.lower() == role.lower():
                return cls.ROLE_CURRICULA[key]
        return cls.ROLE_CURRICULA["Software Engineer"]

    @classmethod
    async def aggregate_user_data(cls, user_id: str) -> Dict[str, Any]:
        user_data = {
            "resume_keywords": [],
            "missing_keywords": [],
            "ats_score": 75,
            "weak_sections": [],
            "coding_attempts": [],
            "solved_problem_ids": [],
            "failed_problem_ids": [],
            "topic_accuracy": {},
            "weak_topics": [],
            "strong_topics": [],
            "interview_sessions": [],
            "avg_interview_score": 80,
            "skill_gap_missing": []
        }

        # 1. Resume scan data
        try:
            scan = await resume_repository.get_latest_user_scan(user_id)
            if scan:
                user_data["resume_keywords"] = scan.get("matched_keywords", [])
                user_data["missing_keywords"] = scan.get("missing_keywords", [])
                user_data["ats_score"] = scan.get("overall_score", 75)
                user_data["weak_sections"] = [w.get("section") for w in scan.get("weak_sections", []) if isinstance(w, dict)]
        except Exception:
            pass

        # 2. Coding Arena data
        try:
            attempts_cursor = coding_repository.col.find({"user_id": str(user_id)})
            attempts = await attempts_cursor.to_list(500)
            user_data["coding_attempts"] = len(attempts)

            topic_stats = {} # topic -> {passed: int, total: int}
            for att in attempts:
                status = att.get("status", "")
                p_id = att.get("problem_id", "")

                # Lookup problem category/topic
                p_seed, top_doc, cat_doc = coding_repository.find_problem_in_seed(p_id)
                topic_name = top_doc.get("title", "Algorithms") if top_doc else "Algorithms"

                if topic_name not in topic_stats:
                    topic_stats[topic_name] = {"passed": 0, "total": 0}

                topic_stats[topic_name]["total"] += 1
                if status == "Accepted":
                    topic_stats[topic_name]["passed"] += 1
                    if p_id not in user_data["solved_problem_ids"]:
                        user_data["solved_problem_ids"].append(p_id)
                else:
                    if p_id not in user_data["failed_problem_ids"]:
                        user_data["failed_problem_ids"].append(p_id)

            for t_name, stats in topic_stats.items():
                acc = round((stats["passed"] / max(1, stats["total"])) * 100)
                user_data["topic_accuracy"][t_name] = acc
                if acc < 60:
                    user_data["weak_topics"].append(t_name)
                elif acc >= 80:
                    user_data["strong_topics"].append(t_name)
        except Exception:
            pass

        # 3. Interview Sessions data
        try:
            sessions = await interview_repository.list_user_sessions(user_id, limit=20)
            user_data["interview_sessions"] = len(sessions)
            if sessions:
                scores = [s.get("overall_score", s.get("score", 75)) for s in sessions if s.get("score") or s.get("overall_score")]
                if scores:
                    user_data["avg_interview_score"] = round(sum(scores) / len(scores))
        except Exception:
            pass

        # 4. Skill Gap data
        try:
            gap_doc = await learning_repository.gap_col.find_one({"user_id": str(user_id)})
            if gap_doc:
                user_data["skill_gap_missing"] = gap_doc.get("missing_skills", [])
        except Exception:
            pass

        return user_data

    @classmethod
    async def generate_or_recalculate_roadmap(
        cls,
        user_id: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        target_role = config.get("target_role", "Software Engineer")
        exp_level = config.get("experience_level", "Entry Level / Fresh Grad")
        company_type = config.get("company_type", "MAANG / Tier-1 Product")
        prep_weeks = int(config.get("prep_time_weeks", 4))
        skill_level = config.get("skill_level", "Intermediate")

        # Fetch existing roadmap to preserve completed items
        existing_doc = await adaptive_roadmap_repository.get_by_user_id(user_id)
        completed_ids = set(existing_doc.get("completed_item_ids", [])) if existing_doc else set()

        # Gather real user performance data across platform repositories
        user_metrics = await cls.aggregate_user_data(user_id)

        # Get raw curriculum template for target role
        raw_items = cls.get_role_template(target_role)

        # Fetch user's bookmarks and resource completion status
        user_bookmarks = await learning_repository.get_user_bookmarks(user_id)
        bookmarked_rids = set(b.get("resource_id") for b in user_bookmarks)
        user_res_progress = await learning_repository.get_user_resource_progress(user_id)

        # Process each item with Adaptive Logic & Rationales
        processed_items = []
        for template in raw_items:
            item = dict(template)
            item_id = item["id"]
            topic_key = item.get("topic_key", "Algorithms")

            # Default completion status
            is_completed = item_id in completed_ids
            item["completion_status"] = "completed" if is_completed else "upcoming"

            # Compute priority & recommendation reason adaptively
            priority = item.get("default_priority", "Medium")
            reasons = []

            # Check weak topic flags from Coding Arena
            is_weak_topic = any(wt.lower() in topic_key.lower() for wt in user_metrics["weak_topics"])
            if is_weak_topic:
                priority = "High"
                reasons.append(f"Identified as a weak topic in recent Coding Arena submissions ({user_metrics['topic_accuracy'].get(topic_key, 0)}% accuracy).")

            # Check missing keywords from ATS scan
            is_missing_ats = any(mk.lower() in item["title"].lower() or mk.lower() in topic_key.lower() for mk in user_metrics["missing_keywords"])
            if is_missing_ats:
                priority = "High"
                reasons.append(f"Missing prerequisite keyword flagged in latest ATS resume analysis.")

            # Check missing skills from Skill Gap Analyzer
            is_missing_gap = any(mg.lower() in item["title"].lower() for mg in user_metrics["skill_gap_missing"])
            if is_missing_gap:
                priority = "High"
                reasons.append("Skill Gap Analyzer flagged this prerequisite as missing for target role.")

            # Check strong topics from Coding Arena
            is_strong_topic = any(st.lower() in topic_key.lower() for st in user_metrics["strong_topics"])
            if is_strong_topic and not is_completed:
                if item["difficulty"] == "Easy":
                    item["difficulty"] = "Medium"
                reasons.append("Strong topic mastery detected in Coding Arena — difficulty accelerated.")

            # Prerequisites reasoning
            if item.get("prerequisites"):
                prereq_titles = []
                for p_id in item["prerequisites"]:
                    p_match = next((t["title"] for t in raw_items if t["id"] == p_id), p_id)
                    prereq_titles.append(p_match)
                prereqs_met = all(p_id in completed_ids for p_id in item["prerequisites"])
                if not prereqs_met:
                    reasons.append(f"Requires prerequisites: {', '.join(prereq_titles)}.")

            if not reasons:
                reasons.append(f"Recommended core milestone for target role '{target_role}'.")

            item["priority"] = priority
            item["reason_for_recommendation"] = " • ".join(reasons)

            # Direct link mapping to Coding Arena category
            item["practice_link"] = f"/coding-arena?topic={topic_key}&role={target_role}"

            # Fetch YouTube learning resources for topic
            raw_resources = YouTubeResourceService.get_resources_for_topic(
                topic=topic_key,
                target_role=target_role,
                user_skill_level=skill_level
            )

            # Decorate resources with user bookmark and completion status
            enriched_resources = []
            for r in raw_resources:
                rid = r["id"]
                prog_info = user_res_progress.get(rid, {})
                enriched_resources.append({
                    **r,
                    "is_bookmarked": rid in bookmarked_rids,
                    "completion_status": prog_info.get("status", "not_started")
                })

            item["learning_resources"] = enriched_resources
            processed_items.append(item)

        # Apply Prerequisite Ordering & High-Priority Topological Sorting
        ordered_items = cls._topological_sort_roadmap(processed_items, completed_ids)

        # Mark next recommended action and current focus
        next_action = None
        current_focus = f"Core Preparation - {target_role}"
        for it in ordered_items:
            if it["completion_status"] != "completed":
                prereqs_met = all(pid in completed_ids for pid in it.get("prerequisites", []))
                if prereqs_met and not next_action:
                    it["completion_status"] = "in_progress"
                    next_action = it
                    current_focus = f"{it['category']} - {it['title']}"
                    break

        total_items = len(ordered_items)
        completed_count = len(completed_ids)
        overall_progress = round((completed_count / max(1, total_items)) * 100, 1)

        roadmap_payload = {
            "user_id": str(user_id),
            "config": {
                "target_role": target_role,
                "experience_level": exp_level,
                "company_type": company_type,
                "prep_time_weeks": prep_weeks,
                "skill_level": skill_level
            },
            "overall_progress": overall_progress,
            "total_tasks": total_items,
            "completed_tasks_count": completed_count,
            "remaining_tasks_count": max(0, total_items - completed_count),
            "completed_item_ids": list(completed_ids),
            "current_focus": current_focus,
            "next_recommended_action": next_action,
            "items": ordered_items,
            "user_performance_summary": {
                "ats_score": user_metrics["ats_score"],
                "coding_attempts": user_metrics["coding_attempts"],
                "weak_topics": user_metrics["weak_topics"],
                "strong_topics": user_metrics["strong_topics"],
                "avg_interview_score": user_metrics["avg_interview_score"]
            }
        }

        return await adaptive_roadmap_repository.save_roadmap(user_id, roadmap_payload)

    @classmethod
    def _topological_sort_roadmap(cls, items: List[Dict[str, Any]], completed_ids: set) -> List[Dict[str, Any]]:

        item_map = {it["id"]: it for it in items}
        ordered = []
        visited = set()

        def visit(item_id, stack):
            if item_id in visited:
                return
            if item_id not in item_map:
                return

            it = item_map[item_id]
            for prereq_id in it.get("prerequisites", []):
                if prereq_id not in stack:
                    visit(prereq_id, stack + [item_id])

            visited.add(item_id)
            ordered.append(it)

        # Priority score helper: High=3, Medium=2, Low=1
        prio_score = {"High": 3, "Medium": 2, "Low": 1}
        sorted_initial = sorted(items, key=lambda x: prio_score.get(x["priority"], 2), reverse=True)

        for item in sorted_initial:
            visit(item["id"], [])

        return ordered

    @classmethod
    async def get_ai_recommended_resources(cls, user_id: str, target_role: Optional[str] = "Software Engineer") -> List[Dict[str, Any]]:
        """
        AI Resource Recommendation Engine:
        Gathers user metrics, identifies weak topics & skill gaps, and returns top recommended
        YouTube resources across all platform modules. NEVER generates unverified/fake YouTube links.
        """
        metrics = await cls.aggregate_user_data(user_id)
        topics_to_target = []

        if metrics["weak_topics"]:
            topics_to_target.extend(metrics["weak_topics"])

        if metrics["skill_gap_missing"]:
            topics_to_target.extend(metrics["skill_gap_missing"])

        if not topics_to_target:
            topics_to_target = ["Arrays", "Dynamic Programming", "SQL", "System Design"]

        recommended = []
        seen_ids = set()

        for topic in topics_to_target:
            resources = YouTubeResourceService.get_resources_for_topic(topic, target_role)
            for res in resources:
                rid = res["id"]
                if rid not in seen_ids:
                    seen_ids.add(rid)
                    recommended.append({
                        **res,
                        "recommendation_reason": f"Targeted recommendation based on performance analysis in '{topic}'."
                    })
                if len(recommended) >= 6:
                    break
            if len(recommended) >= 6:
                break

        return recommended
