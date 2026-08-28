from typing import Dict, Any, List, Optional
from datetime import datetime
from app.repositories.resume_repository import resume_repository
from app.repositories.coding_repository import CodingRepository
from app.repositories.interview_repository import InterviewRepository
from app.repositories.learning_repository import learning_repository
from app.repositories.company_prep_repository import company_prep_repository

coding_repository = CodingRepository()
interview_repository = InterviewRepository()

class CompanyPrepService:

    COMPANY_CATALOG = {
        "ibm": {
            "id": "ibm",
            "name": "IBM",
            "logo": "🟦",
            "tier": "Global Tech Enterprise",
            "avg_ctc": "₹10 - 18 LPA",
            "difficulty": "Medium - Hard",
            "supported_roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Cloud Engineer", "Data Scientist"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["Java", "Python", "Data Structures", "REST APIs", "SQL", "Cloud Fundamentals", "Docker"],
                    "coding_topics": ["Arrays & Hashing", "Strings", "Trees", "Graphs", "Dynamic Programming"],
                    "cs_fundamentals": ["Object-Oriented Programming (OOP)", "Operating Systems", "DBMS", "Computer Networks"],
                    "sql_topics": ["Joins & Group By", "Subqueries", "Aggregations", "Indexing"],
                    "behavioral_topics": ["Growth Mindset", "Team Collaboration", "Agile Ownership", "Technical Decision Rationale"],
                    "rounds": [
                        {"round": 1, "name": "Cognitive & Coding Assessment (OA)", "type": "HackerRank (2 Coding + Cognitive)", "duration": "90 mins"},
                        {"round": 2, "name": "Technical Round 1", "type": "Core DSA & System Concepts", "duration": "60 mins"},
                        {"round": 3, "name": "Technical Round 2", "type": "Project Architecture & APIs", "duration": "45 mins"},
                        {"round": 4, "name": "HR / Managerial Round", "type": "Behavioral & Cultural Fit", "duration": "30 mins"}
                    ]
                },
                "Full Stack Developer": {
                    "required_skills": ["React.js", "Node.js", "JavaScript", "TypeScript", "REST APIs", "MongoDB", "Docker"],
                    "coding_topics": ["Arrays", "Strings", "Hash Tables", "DOM Manipulation", "Promises & Async"],
                    "cs_fundamentals": ["Web Performance", "API Design", "OOP", "DBMS"],
                    "sql_topics": ["Relational vs NoSQL", "Indexing", "Aggregations"],
                    "behavioral_topics": ["Cross-functional Teamwork", "Customer Centricity", "Delivering Under Deadlines"],
                    "rounds": [
                        {"round": 1, "name": "Full Stack OA", "type": "Frontend + Backend Challenge", "duration": "90 mins"},
                        {"round": 2, "name": "Technical Deep Dive", "type": "System Architecture & Live Coding", "duration": "60 mins"},
                        {"round": 3, "name": "Managerial Round", "type": "Project & Behavioral Evaluation", "duration": "45 mins"}
                    ]
                }
            }
        },
        "google": {
            "id": "google",
            "name": "Google",
            "logo": "🔍",
            "tier": "MAANG / Big Tech",
            "avg_ctc": "₹25 - 45 LPA",
            "difficulty": "Very Hard",
            "supported_roles": ["Software Engineer", "Backend Developer", "Machine Learning Engineer", "Data Scientist"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["C++", "Java", "Python", "Advanced Algorithms", "Graph Theory", "System Design"],
                    "coding_topics": ["Graph Algorithms (BFS/DFS/Dijkstra)", "Dynamic Programming", "Segment Trees", "Tries", "Bit Manipulation"],
                    "cs_fundamentals": ["Operating Systems", "Concurrency & Threading", "Distributed Systems", "Computer Architecture"],
                    "sql_topics": ["Complex Aggregations", "Window Functions", "Query Optimization"],
                    "behavioral_topics": ["Googleyness & Leadership", "Handling Ambiguity", "Conflict Resolution", "Bias for Action"],
                    "rounds": [
                        {"round": 1, "name": "Online Coding Screen", "type": "2 Advanced Algorithmic Problems", "duration": "90 mins"},
                        {"round": 2, "name": "Technical Interview 1", "type": "Graph & Tree Optimization", "duration": "45 mins"},
                        {"round": 3, "name": "Technical Interview 2", "type": "Dynamic Programming & Strings", "duration": "45 mins"},
                        {"round": 4, "name": "Googleyness Round", "type": "Behavioral & Cultural Alignment", "duration": "45 mins"}
                    ]
                }
            }
        },
        "amazon": {
            "id": "amazon",
            "name": "Amazon",
            "logo": "📦",
            "tier": "MAANG / Big Tech",
            "avg_ctc": "₹20 - 32 LPA",
            "difficulty": "Hard",
            "supported_roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Cloud Engineer"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["Java", "C++", "Object-Oriented Design", "AWS", "Data Structures", "System Design"],
                    "coding_topics": ["Trees & Binary Search Trees", "Graphs (Topological Sort)", "Dynamic Programming", "Priority Queues"],
                    "cs_fundamentals": ["Object-Oriented Design (LLD)", "Operating Systems", "DBMS", "Networking"],
                    "sql_topics": ["Complex Joins", "Aggregations", "Indexing"],
                    "behavioral_topics": ["Amazon 16 Leadership Principles", "Customer Obsession", "Ownership", "Dive Deep"],
                    "rounds": [
                        {"round": 1, "name": "Online Assessment (OA)", "type": "2 Coding + Work Style Assessment", "duration": "90 mins"},
                        {"round": 2, "name": "Technical Round 1", "type": "DSA & Coding", "duration": "60 mins"},
                        {"round": 3, "name": "Technical Round 2", "type": "Low-Level Design (LLD)", "duration": "60 mins"},
                        {"round": 4, "name": "Bar Raiser Round", "type": "Leadership Principles (STAR Method)", "duration": "60 mins"}
                    ]
                }
            }
        },
        "microsoft": {
            "id": "microsoft",
            "name": "Microsoft",
            "logo": "🪟",
            "tier": "MAANG / Big Tech",
            "avg_ctc": "₹18 - 30 LPA",
            "difficulty": "Hard",
            "supported_roles": ["Software Engineer", "Full Stack Developer", "Cloud Engineer", "Data Engineer"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["C#", "C++", "Java", "Azure", "Data Structures", "System Architecture"],
                    "coding_topics": ["Linked Lists", "Trees", "Arrays", "String Manipulation", "Recursion & Backtracking"],
                    "cs_fundamentals": ["Operating Systems", "Memory Management", "DBMS", "OOP"],
                    "sql_topics": ["Group By", "Subqueries", "Joins"],
                    "behavioral_topics": ["Growth Mindset", "Customer Empathy", "Diversity & Inclusion", "Technical Passion"],
                    "rounds": [
                        {"round": 1, "name": "Codility OA", "type": "3 Algorithmic Challenges", "duration": "75 mins"},
                        {"round": 2, "name": "Technical Round 1", "type": "Data Structures & Code Quality", "duration": "60 mins"},
                        {"round": 3, "name": "Technical Round 2", "type": "System Design & Problem Solving", "duration": "60 mins"},
                        {"round": 4, "name": "AA Round (As-Appropriate)", "type": "Executive Alignment & Culture", "duration": "45 mins"}
                    ]
                }
            }
        },
        "meta": {
            "id": "meta",
            "name": "Meta (Facebook)",
            "logo": "♾️",
            "tier": "MAANG / Big Tech",
            "avg_ctc": "₹28 - 50 LPA",
            "difficulty": "Very Hard",
            "supported_roles": ["Software Engineer", "Frontend Developer", "Backend Developer", "Data Engineer"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["Python", "C++", "JavaScript", "React", "Distributed Systems", "Algorithms"],
                    "coding_topics": ["Binary Search", "Trees", "Graphs", "Sliding Window", "Two Pointers"],
                    "cs_fundamentals": ["System Architecture", "Concurrency", "DBMS", "Networking"],
                    "sql_topics": ["Window Functions", "Date/Time Operations", "Group Aggregations"],
                    "behavioral_topics": ["Move Fast", "Build Awesome Things", "Be Direct & Respectful"],
                    "rounds": [
                        {"round": 1, "name": "Initial Technical Screen", "type": "2 Medium/Hard Coding Problems", "duration": "45 mins"},
                        {"round": 2, "name": "Coding Onsite 1", "type": "Fast Problem Solving & Clean Code", "duration": "45 mins"},
                        {"round": 3, "name": "System Design Onsite", "type": "Large-Scale Architecture", "duration": "45 mins"},
                        {"round": 4, "name": "Behavioral Onsite", "type": "Past Experience & Meta Culture", "duration": "45 mins"}
                    ]
                }
            }
        },
        "tcs": {
            "id": "tcs",
            "name": "TCS (Tata Consultancy Services)",
            "logo": "🏛️",
            "tier": "IT Services Leader",
            "avg_ctc": "₹4 - 9 LPA",
            "difficulty": "Easy - Medium",
            "supported_roles": ["Software Engineer", "Full Stack Developer", "System Engineer", "Data Analyst"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["Java", "Python", "C", "SQL", "HTML/CSS", "SDLC"],
                    "coding_topics": ["Strings", "Arrays", "Basic Math Algorithms", "Sorting & Searching"],
                    "cs_fundamentals": ["OOP Concepts", "DBMS Basics", "C Programming", "Software Engineering"],
                    "sql_topics": ["Basic Select", "Where Clause", "Group By", "Joins"],
                    "behavioral_topics": ["Punctuality", "Flexibility", "Client Orientation", "Team Ethics"],
                    "rounds": [
                        {"round": 1, "name": "TCS NQT Assessment", "type": "Aptitude + Reasoning + Coding", "duration": "120 mins"},
                        {"round": 2, "name": "Technical Interview", "type": "Fundamentals & Resume Projects", "duration": "30 mins"},
                        {"round": 3, "name": "HR & Managerial Round", "type": "Communication & Relocation Check", "duration": "20 mins"}
                    ]
                }
            }
        },
        "infosys": {
            "id": "infosys",
            "name": "Infosys",
            "logo": "💻",
            "tier": "IT Services Leader",
            "avg_ctc": "₹4.5 - 9.5 LPA",
            "difficulty": "Easy - Medium",
            "supported_roles": ["Software Engineer", "System Engineer", "Full Stack Developer"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["Java", "Python", "SQL", "OOP", "Data Structures"],
                    "coding_topics": ["Arrays", "Strings", "Recursion", "Sorting"],
                    "cs_fundamentals": ["DBMS", "OOP", "Operating Systems", "Software Design"],
                    "sql_topics": ["Queries", "Joins", "Aggregations"],
                    "behavioral_topics": ["Adaptability", "Learning Agility", "Professional Integrity"],
                    "rounds": [
                        {"round": 1, "name": "InfyTQ / HackWithInfy", "type": "Coding & Aptitude Test", "duration": "100 mins"},
                        {"round": 2, "name": "Technical Interview", "type": "Coding + Core CS Topics", "duration": "45 mins"},
                        {"round": 3, "name": "HR Round", "type": "Behavioral Evaluation", "duration": "20 mins"}
                    ]
                }
            }
        },
        "wipro": {
            "id": "wipro",
            "name": "Wipro",
            "logo": "🌐",
            "tier": "IT Services Leader",
            "avg_ctc": "₹4.2 - 8.5 LPA",
            "difficulty": "Easy - Medium",
            "supported_roles": ["Software Engineer", "System Engineer", "Cloud Associate"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["Java", "C++", "Python", "SQL", "Cloud Basics"],
                    "coding_topics": ["Arrays", "Strings", "Basic Algorithms"],
                    "cs_fundamentals": ["OOP", "DBMS", "Networking Basics"],
                    "sql_topics": ["Basic Queries", "Joins"],
                    "behavioral_topics": ["Team Collaboration", "Problem Solving", "Growth Orientation"],
                    "rounds": [
                        {"round": 1, "name": "NLTH Assessment", "type": "Aptitude + Essay + 2 Coding", "duration": "120 mins"},
                        {"round": 2, "name": "Technical & HR Interview", "type": "Combined Technical + Fit", "duration": "40 mins"}
                    ]
                }
            }
        },
        "accenture": {
            "id": "accenture",
            "name": "Accenture",
            "logo": "⚡",
            "tier": "Global Consulting & Tech",
            "avg_ctc": "₹5 - 11 LPA",
            "difficulty": "Medium",
            "supported_roles": ["Software Engineer", "Full Stack Developer", "Cloud Engineer"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["Java", "Python", "JavaScript", "SQL", "Cloud Services", "Agile"],
                    "coding_topics": ["Arrays", "Strings", "Bitwise Operations", "Matrices"],
                    "cs_fundamentals": ["Pseudocode Analysis", "Networking", "DBMS", "OOP"],
                    "sql_topics": ["Data Retrieval", "Joins", "Aggregation Functions"],
                    "behavioral_topics": ["Client Communication", "Analytical Thinking", "Continuous Learning"],
                    "rounds": [
                        {"round": 1, "name": "Cognitive & Technical Assessment", "type": "90 Questions (Reasoning + Tech)", "duration": "90 mins"},
                        {"round": 2, "name": "Coding Assessment", "type": "2 Algorithmic Coding Problems", "duration": "45 mins"},
                        {"round": 3, "name": "Communication Assessment", "type": "Automated Speech & Listening", "duration": "20 mins"},
                        {"round": 4, "name": "Technical Interview", "type": "Project Review & HR Fit", "duration": "30 mins"}
                    ]
                }
            }
        },
        "uber": {
            "id": "uber",
            "name": "Uber",
            "logo": "🚗",
            "tier": "Top Tech Product",
            "avg_ctc": "₹26 - 42 LPA",
            "difficulty": "Hard",
            "supported_roles": ["Software Engineer", "Backend Developer", "Data Scientist"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["Go", "Java", "C++", "Distributed Systems", "Graph Algorithms", "Kafka"],
                    "coding_topics": ["Graphs & Shortest Paths", "Dynamic Programming", "Heaps", "Concurrency"],
                    "cs_fundamentals": ["High Scale Architecture", "Distributed Systems", "DBMS", "Concurrency"],
                    "sql_topics": ["Complex Aggregations", "Window Functions", "Performance Tuning"],
                    "behavioral_topics": ["Go Get It", "Customer Obsession", "One Uber", "Build with Heart"],
                    "rounds": [
                        {"round": 1, "name": "Online Coding Screen", "type": "3 Hard Algorithmic Problems", "duration": "75 mins"},
                        {"round": 2, "name": "DSA Coding Onsite 1", "type": "Graph & Optimization", "duration": "60 mins"},
                        {"round": 3, "name": "System Design Onsite", "type": "Real-time Location & Routing System", "duration": "60 mins"},
                        {"round": 4, "name": "Bar Raiser / Fit", "type": "Uber Cultural Alignment", "duration": "45 mins"}
                    ]
                }
            }
        },
        "flipkart": {
            "id": "flipkart",
            "name": "Flipkart",
            "logo": "🛍️",
            "tier": "E-Commerce Unicorn",
            "avg_ctc": "₹18 - 28 LPA",
            "difficulty": "Hard",
            "supported_roles": ["Software Engineer", "Full Stack Developer", "Backend Developer", "Data Engineer"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["Java", "Python", "Machine Coding", "LLD", "Spring Boot", "Kafka"],
                    "coding_topics": ["Machine Coding (LLD)", "Arrays & Hashing", "Trees", "Graphs", "DP"],
                    "cs_fundamentals": ["Object-Oriented Design", "Concurrency", "DBMS", "API Design"],
                    "sql_topics": ["Database Schema Design", "Indexes", "Queries"],
                    "behavioral_topics": ["Customer First", "Audacity", "Bias for Action", "Integrity"],
                    "rounds": [
                        {"round": 1, "name": "Online Coding Assessment", "type": "3 Coding Challenges", "duration": "90 mins"},
                        {"round": 2, "name": "Machine Coding Round", "type": "Live Object-Oriented Code Design", "duration": "90 mins"},
                        {"round": 3, "name": "Problem Solving & DSA", "type": "Trees, Graphs, DP", "duration": "60 mins"},
                        {"round": 4, "name": "Managerial Round", "type": "Past Work & Cultural Fit", "duration": "45 mins"}
                    ]
                }
            }
        },
        "razorpay": {
            "id": "razorpay",
            "name": "Razorpay",
            "logo": "💳",
            "tier": "FinTech Unicorn",
            "avg_ctc": "₹16 - 26 LPA",
            "difficulty": "Hard",
            "supported_roles": ["Software Engineer", "Full Stack Developer", "Backend Developer"],
            "default_role": "Software Engineer",
            "roles_config": {
                "Software Engineer": {
                    "required_skills": ["Go", "Node.js", "Java", "MySQL", "Redis", "Distributed Transactions"],
                    "coding_topics": ["Machine Coding (LLD)", "Arrays", "Dynamic Programming", "Trees"],
                    "cs_fundamentals": ["Transactions & Idempotency", "Database Indexing", "OOP", "Concurrency"],
                    "sql_topics": ["ACID Properties", "Transactions", "Joins"],
                    "behavioral_topics": ["Customer First", "Ownership", "First Principles Thinking"],
                    "rounds": [
                        {"round": 1, "name": "HackerRank OA", "type": "2 Coding Problems", "duration": "60 mins"},
                        {"round": 2, "name": "DSA & Problem Solving", "type": "Arrays, DP, Trees", "duration": "60 mins"},
                        {"round": 3, "name": "System Design / Backend", "type": "Idempotent Gateway & Redis", "duration": "60 mins"},
                        {"round": 4, "name": "Culture Fit", "type": "Ownership & Problem Solving", "duration": "45 mins"}
                    ]
                }
            }
        }
    }

    @classmethod
    def get_catalog(cls) -> List[Dict[str, Any]]:
        result = []
        for cid, comp in cls.COMPANY_CATALOG.items():
            result.append({
                "id": comp["id"],
                "name": comp["name"],
                "logo": comp["logo"],
                "tier": comp["tier"],
                "avg_ctc": comp["avg_ctc"],
                "difficulty": comp["difficulty"],
                "supported_roles": comp["supported_roles"],
                "default_role": comp["default_role"]
            })
        return result

    @classmethod
    async def get_company_prep_plan(cls, user_id: str, company_id: str, target_role: Optional[str] = None) -> Dict[str, Any]:
        user_id_str = str(user_id)
        cid = company_id.lower() if company_id else "ibm"
        comp_meta = cls.COMPANY_CATALOG.get(cid, cls.COMPANY_CATALOG["ibm"])

        role = target_role if target_role in comp_meta["supported_roles"] else comp_meta["default_role"]
        roles_cfg = comp_meta["roles_config"].get(role, list(comp_meta["roles_config"].values())[0])

        # 1. Fetch Candidate Actual Performance Data
        scan = await resume_repository.get_latest_user_scan(user_id_str)
        coding_cursor = coding_repository.col.find({"user_id": user_id_str})
        coding_attempts = await coding_cursor.to_list(500)
        interview_sessions = await interview_repository.list_user_sessions(user_id_str, limit=50)
        gap_doc = await learning_repository.gap_col.find_one({"user_id": user_id_str})

        # 2. Derive Verified Candidate Skills
        user_skills = []
        if scan:
            user_skills.extend(scan.get("matched_keywords", []))
            struct_skills = scan.get("structured_extraction", {}).get("skills", {})
            if isinstance(struct_skills, dict):
                user_skills.extend(struct_skills.get("technical", []))
                user_skills.extend(struct_skills.get("tools", []))
        if gap_doc and gap_doc.get("user_skills"):
            user_skills.extend(gap_doc.get("user_skills"))

        user_skills = list(dict.fromkeys([s for s in user_skills if s]))

        # 3. Required vs Missing Skills
        required_skills = roles_cfg["required_skills"]
        user_skills_lower = [s.lower() for s in user_skills]
        missing_skills = [req for req in required_skills if req.lower() not in user_skills_lower]
        matched_skills = [req for req in required_skills if req.lower() in user_skills_lower]
        skill_overlap_pct = round((len(matched_skills) / max(1, len(required_skills))) * 100, 1)

        # 4. Resume ATS Match Score
        resume_match_score = scan.get("overall_score", 50) if scan else 45

        # 5. Coding Topic Accuracy for Company Topics
        comp_topics = roles_cfg["coding_topics"]
        matching_coding_attempts = []
        for att in coding_attempts:
            p_id = att.get("problem_id", "")
            p_seed, top_doc, cat_doc = coding_repository.find_problem_in_seed(p_id)
            top_title = top_doc.get("title", "") if top_doc else ""
            if any(t.lower() in top_title.lower() for t in comp_topics) or not comp_topics:
                matching_coding_attempts.append(att)

        if coding_attempts:
            solved_cnt = sum(1 for c in coding_attempts if c.get("status") in ["Accepted", "Passed", "Success"])
            coding_readiness = round((solved_cnt / len(coding_attempts)) * 100, 1)
        else:
            coding_readiness = 40.0

        # 6. Interview Readiness
        if interview_sessions:
            scores = [s.get("overall_score", s.get("score", 70)) for s in interview_sessions if s.get("score") or s.get("overall_score")]
            interview_readiness = round(sum(scores) / len(scores), 1) if scores else 65.0
        else:
            interview_readiness = 50.0

        # 7. Weighted Company-Role Readiness Index
        overall_readiness = round(
            (0.25 * resume_match_score) +
            (0.30 * coding_readiness) +
            (0.25 * interview_readiness) +
            (0.20 * skill_overlap_pct),
            1
        )

        # 8. Filter Recommended Problems from existing Coding Arena seed
        all_seed_problems = coding_repository.SEED_PROBLEMS
        recommended_questions = []
        for p in all_seed_problems:
            cat_name = p.get("category", "")
            if any(t.lower() in cat_name.lower() or cat_name.lower() in t.lower() for t in comp_topics):
                recommended_questions.append({
                    "id": p.get("id"),
                    "title": p.get("title"),
                    "difficulty": p.get("difficulty"),
                    "category": p.get("category"),
                    "topic": p.get("topic")
                })
        if not recommended_questions:
            recommended_questions = [
                {"id": p["id"], "title": p["title"], "difficulty": p["difficulty"], "category": p["category"]}
                for p in all_seed_problems[:4]
            ]

        # Disclaimer
        disclaimer = (
            "NOTICE: Preparation guidance is based on publicly available engineering hiring patterns, "
            "standard industry benchmarks, and AI recommendations. Generated recommendations do not represent "
            "exact leaked exam questions or guaranteed hiring criteria."
        )

        plan = {
            "user_id": user_id_str,
            "company": {
                "id": comp_meta["id"],
                "name": comp_meta["name"],
                "logo": comp_meta["logo"],
                "tier": comp_meta["tier"],
                "avg_ctc": comp_meta["avg_ctc"],
                "difficulty": comp_meta["difficulty"]
            },
            "target_role": role,
            "supported_roles": comp_meta["supported_roles"],
            "readiness_summary": {
                "overall_readiness": overall_readiness,
                "coding_readiness": coding_readiness,
                "interview_readiness": interview_readiness,
                "resume_match_score": resume_match_score,
                "skill_overlap_pct": skill_overlap_pct
            },
            "skills_analysis": {
                "required_skills": required_skills,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills
            },
            "preparation_topics": {
                "coding_topics": comp_topics,
                "cs_fundamentals": roles_cfg["cs_fundamentals"],
                "sql_topics": roles_cfg["sql_topics"],
                "behavioral_topics": roles_cfg["behavioral_topics"]
            },
            "rounds_breakdown": roles_cfg["rounds"],
            "recommended_questions": recommended_questions[:6],
            "disclaimer": disclaimer,
            "calculated_at": datetime.utcnow().isoformat()
        }

        # Persist candidate company prep snapshot
        await company_prep_repository.save_prep_selection(user_id_str, cid, role, plan)
        return plan
