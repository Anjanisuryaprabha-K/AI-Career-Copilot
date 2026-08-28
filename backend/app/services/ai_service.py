import re
import random
from typing import Dict, Any, List, Optional
from app.services.search_service import SearchService

TECH_QUESTION_BANK = {
    "Full Stack Developer": [
        "Explain the request-response lifecycle when a React client calls a REST API built with Express/FastAPI and MongoDB.",
        "What is the difference between SQL and NoSQL databases? When would you choose MongoDB over PostgreSQL?",
        "How do you handle JWT authentication, token storage, and secure token revocation using Redis?",
        "What is middleware in Express/FastAPI, and how does error-handling middleware differ from standard route middleware?",
        "Explain how the JavaScript Event Loop handles microtasks (Promises) versus macrotasks (setTimeout)."
    ],
    "Frontend Developer": [
        "Explain the difference between state and props in React, and how React 18 Fiber reconciliation triggers re-renders.",
        "What is the difference between REST and GraphQL APIs? What problem does GraphQL solve regarding over-fetching?",
        "How do you optimize Web Vitals (LCP, CLS, FID) for a modern React single-page application?",
        "Explain how CSS `box-sizing: border-box` works and how Flexbox differs from Grid layout math."
    ],
    "Backend Developer": [
        "Explain how database indexing works under the hood. What are the trade-offs of using B-Tree vs Hash indexes?",
        "How does FastAPI manage asynchronous concurrency with `async def` and `await` using the Uvicorn event loop?",
        "How would you design a distributed Rate Limiter using Redis Token Bucket or Sliding Window log algorithm?",
        "Explain the CAP theorem and PACELC extension. Give a real-world example of an AP vs CP database choice."
    ],
    "Python Developer": [
        "How do Python list comprehensions, generators, and iterators differ in terms of memory utilization?",
        "Explain Python GIL (Global Interpreter Lock) and how multiprocessing differs from multithreading for CPU-bound tasks.",
        "How do Python decorators work under the hood, and how do you write a decorator that accepts custom arguments?"
    ],
    "Data Scientist": [
        "Explain the bias-variance trade-off in machine learning models and how regularization (L1 vs L2) mitigates overfitting.",
        "What is the difference between Bagging (Random Forests) and Boosting (XGBoost/LightGBM)?",
        "How do transformer self-attention mechanisms work compared to traditional Recurrent Neural Networks (RNNs)?"
    ]
}

class AIService:
    @classmethod
    def generate_personalized_question(
        cls,
        session: Dict[str, Any],
        user_profile: Optional[Dict[str, Any]] = None,
        resume_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        role = session.get("role", "Full Stack Developer")
        experience = session.get("experience_level", "Fresher")
        interview_type = session.get("interview_type", "Technical")
        difficulty = session.get("difficulty", "Adaptive")
        tech_list = session.get("technologies", [])
        asked_questions = [q.get("question", "") for q in session.get("questions", [])]

        # Extract resume skills if available
        resume_skills = []
        if resume_data and "matched_keywords" in resume_data:
            resume_skills = resume_data.get("matched_keywords", [])

        # Match question pool based on role
        pool_key = "Full Stack Developer"
        for k in TECH_QUESTION_BANK:
            if k.lower() in role.lower() or role.lower() in k.lower():
                pool_key = k
                break

        candidates = [q for q in TECH_QUESTION_BANK[pool_key] if q not in asked_questions]
        if not candidates:
            candidates = [
                f"How would you optimize performance and handle edge cases when building a scalable feature with {tech_list[0] if tech_list else 'modern frameworks'}?",
                f"Explain a challenging technical bug you encountered in a {role} project and how you debugged and resolved it."
            ]

        selected_q = candidates[0]

        # Context topic mapping
        topic = "General Technical"
        if "database" in selected_q.lower() or "sql" in selected_q.lower() or "mongodb" in selected_q.lower():
            topic = "Databases & Persistence"
        elif "react" in selected_q.lower() or "state" in selected_q.lower() or "css" in selected_q.lower():
            topic = "Frontend Architecture"
        elif "async" in selected_q.lower() or "jwt" in selected_q.lower() or "middleware" in selected_q.lower() or "fastapi" in selected_q.lower():
            topic = "Backend & Security"
        elif "rate limit" in selected_q.lower() or "cap" in selected_q.lower():
            topic = "System Design & Architecture"

        return {
            "question_index": len(session.get("questions", [])) + 1,
            "question": selected_q,
            "topic": topic,
            "difficulty": difficulty,
            "personalized_note": f"Prioritized based on {role} role and skills: {', '.join(tech_list[:3] or ['Core Concepts'])}."
        }

    @classmethod
    async def evaluate_semantic_answer(
        cls,
        question: str,
        candidate_answer: str,
        role: str = "Full Stack Developer",
        experience_level: str = "Fresher"
    ) -> Dict[str, Any]:
        ans_clean = candidate_answer.strip().lower()
        words = ans_clean.split()
        word_count = len(words)

        if word_count < 5:
            return {
                "question_score": 35,
                "metrics": {
                    "correctness": 30,
                    "relevance": 40,
                    "completeness": 25,
                    "technical_depth": 30,
                    "communication": 50
                },
                "evaluation_text": "Answer is extremely brief. Missing core technical concepts and explanations.",
                "expected_concepts": ["Core definition", "Practical implementation example", "Trade-offs"],
                "missing_concepts": ["Detailed explanation", "Real-world trade-offs"],
                "improvement_tips": "Elaborate on the underlying mechanics and give a concrete code or system example.",
                "what_was_wrong": "The answer contained insufficient detail to verify technical understanding.",
                "correct_explanation": f"For '{question}': Provide the core mechanism, runtime complexity or architecture impact, and a practical example.",
                "recommended_learning": "Review fundamental concepts and practice verbalizing technical explanations.",
                "verification_sources": []
            }

        # Verify claims using SearchService
        verification = await SearchService.verify_claim(question, candidate_answer)

        # Keyword semantic indicators
        tech_terms = [
            "component", "middleware", "express", "fastapi", "python", "react", "mongodb", "postgresql",
            "index", "b-tree", "redis", "jwt", "async", "await", "event loop", "promises", "tradeoff",
            "microservice", "latency", "throughput", "schema", "rest", "graphql", "endpoint"
        ]
        hits = [t for t in tech_terms if t in ans_clean]

        # Calculate semantic scores (0 - 100)
        correctness = min(98, max(45, 55 + (len(hits) * 8) + (10 if word_count > 25 else 0)))
        relevance = min(98, max(50, 60 + (15 if any(k in ans_clean for k in question.lower().split() if len(k) > 4) else 5)))
        completeness = min(98, max(40, 50 + (len(hits) * 7) + (15 if "example" in ans_clean or "because" in ans_clean else 0)))
        depth = min(98, max(40, 45 + (len(hits) * 9) + (10 if "tradeoff" in ans_clean or "performance" in ans_clean else 0)))
        communication = min(98, max(55, 65 + (15 if word_count >= 25 else 5)))

        overall_score = round((0.30 * correctness) + (0.20 * relevance) + (0.20 * completeness) + (0.15 * depth) + (0.15 * communication))

        # Expected & Missing Concepts
        expected = [
            "Clear technical definition of terms",
            "Practical framework/system implementation context",
            "Trade-offs & performance considerations"
        ]
        missing = []
        if "tradeoff" not in ans_clean and "performance" not in ans_clean:
            missing.append("Explicitly discussing performance trade-offs or scalability limits.")
        if "example" not in ans_clean:
            missing.append("Providing a concrete real-world implementation example.")

        return {
            "question_score": overall_score,
            "metrics": {
                "correctness": correctness,
                "relevance": relevance,
                "completeness": completeness,
                "technical_depth": depth,
                "communication": communication
            },
            "evaluation_text": "Exemplary technical response demonstrating strong architectural understanding!" if overall_score >= 85 else "Well-structured response covering the core prompt. Adding trade-offs will improve your depth score.",
            "expected_concepts": expected,
            "missing_concepts": missing or ["None - Good coverage of key concepts!"],
            "improvement_tips": "Mention runtime complexity (Big-O) or architectural trade-offs to achieve top marks.",
            "what_was_wrong": None if overall_score >= 70 else "Missed key framework mechanisms and edge-case handling.",
            "correct_explanation": f"Key benchmark: Clearly define the core mechanism of {question}, compare trade-offs, and outline production resilience.",
            "recommended_learning": f"Deep-dive into {hits[0].title() if hits else 'Core Architecture'} technical documentation.",
            "verification_sources": verification.get("sources", [])
        }

    @classmethod
    def generate_adaptive_followup(cls, question: str, candidate_answer: str, last_score: int) -> str:
        if last_score >= 80:
            return f"Great answer! Building on that, how would you architect this to handle 100x traffic spikes while maintaining sub-50ms latency?"
        elif last_score >= 60:
            return f"Good overview. Can you give a concrete real-world example of where you implemented this in a past project?"
        else:
            return f"Let's break this down to fundamentals. What problem does this solve in a standard production application?"

    @classmethod
    def generate_final_report(cls, session: Dict[str, Any]) -> Dict[str, Any]:
        answers = session.get("answers", [])
        questions = session.get("questions", [])

        if not answers:
            return {
                "session_id": session.get("session_id", ""),
                "overall_score": 75,
                "performance_bars": {
                    "technical_knowledge": 75,
                    "problem_solving": 72,
                    "communication": 80,
                    "depth_of_understanding": 70,
                    "accuracy": 76
                },
                "strong_areas": ["Completed setup"],
                "weak_areas": ["Answer questions in detail"],
                "recommended_topics": ["Core Technical Fundamentals"],
                "question_reviews": [],
                "verified_sources": []
            }

        scores = [a.get("evaluation", {}).get("question_score", 75) for a in answers]
        overall_score = round(sum(scores) / len(scores))

        all_sources = []
        all_missing = []
        for a in answers:
            ev = a.get("evaluation", {})
            all_sources.extend(ev.get("verification_sources", []))
            all_missing.extend(ev.get("missing_concepts", []))

        # Unique sources by URL
        unique_sources = []
        seen_urls = set()
        for s in all_sources:
            if s.get("url") not in seen_urls:
                seen_urls.add(s.get("url"))
                unique_sources.append(s)

        return {
            "session_id": session.get("session_id", ""),
            "role": session.get("role", "Full Stack Developer"),
            "experience_level": session.get("experience_level", "Fresher"),
            "overall_score": overall_score,
            "performance_bars": {
                "technical_knowledge": min(98, overall_score + 2),
                "problem_solving": min(98, max(50, overall_score - 3)),
                "communication": min(98, overall_score + 4),
                "depth_of_understanding": min(98, max(50, overall_score - 5)),
                "accuracy": overall_score
            },
            "strong_areas": [
                f"Core {session.get('role', 'Developer')} concepts",
                "Technical terminology & communication",
                "Application workflow understanding"
            ],
            "weak_areas": list(dict.fromkeys(all_missing))[:3] or ["Architectural trade-offs under high scale"],
            "recommended_topics": [
                "Database indexing & query optimization",
                "API rate-limiting & caching strategies",
                "Asynchronous concurrency models"
            ],
            "question_reviews": [
                {
                    "question_number": idx + 1,
                    "question": a.get("question", ""),
                    "candidate_transcript": a.get("candidate_answer", ""),
                    "score": a.get("evaluation", {}).get("question_score", 75),
                    "metrics": a.get("evaluation", {}).get("metrics", {}),
                    "evaluation_text": a.get("evaluation", {}).get("evaluation_text", ""),
                    "expected_concepts": a.get("evaluation", {}).get("expected_concepts", []),
                    "missing_concepts": a.get("evaluation", {}).get("missing_concepts", []),
                    "improvement_tips": a.get("evaluation", {}).get("improvement_tips", ""),
                    "what_was_wrong": a.get("evaluation", {}).get("what_was_wrong"),
                    "correct_explanation": a.get("evaluation", {}).get("correct_explanation", ""),
                    "recommended_learning": a.get("evaluation", {}).get("recommended_learning", "")
                } for idx, a in enumerate(answers)
            ],
            "verified_sources": unique_sources[:5]
        }

