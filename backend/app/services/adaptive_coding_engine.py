from typing import Dict, Any, List, Optional
from datetime import datetime
from app.repositories.coding_repository import CodingRepository
from app.data.problems_seed import ARENA_CATEGORIES_DATA

coding_repository = CodingRepository()

def sanitize_problem(p: Dict[str, Any]) -> Dict[str, Any]:
    if not p:
        return {}
    res = dict(p)
    res.pop("reference_solution", None)
    res.pop("hidden_test_cases", None)
    res.pop("solution", None)
    res.pop("expected_solution", None)
    res.pop("answer", None)
    res.pop("internal_solution", None)
    return res

class AdaptiveCodingEngine:

    @classmethod
    async def get_user_coding_profile(cls, user_id: str) -> Dict[str, Any]:
        user_id_str = str(user_id)
        progress = await coding_repository.get_user_arena_progress(user_id_str)
        history = await coding_repository.get_user_history(user_id_str, limit=200)

        solved_set = set(progress.get("completedProblems", []))
        attempted_set = set(progress.get("attemptedProblems", []))

        # Recent 5 attempts
        recent_attempts = [h.get("problem_id") for h in history[:5] if h.get("problem_id")]

        # Topic & Difficulty performance aggregation
        topic_stats = {} # topic_name -> {attempts: 0, solved: 0, easy_solved: 0, med_solved: 0, hard_solved: 0}
        all_seed_problems = coding_repository.get_all_seed_problems()

        for p in all_seed_problems:
            t_title = p.get("topic_title", p.get("category_title", "Arrays"))
            if t_title not in topic_stats:
                topic_stats[t_title] = {
                    "attempts": 0,
                    "solved": 0,
                    "easy_solved": 0,
                    "medium_solved": 0,
                    "hard_solved": 0
                }

        for h in history:
            pid = h.get("problem_id")
            p_seed, top_doc, cat_doc = coding_repository.find_problem_in_seed(pid)
            t_title = top_doc.get("title", "Arrays") if top_doc else "Arrays"
            diff = p_seed.get("difficulty", "Medium") if p_seed else "Medium"
            st = h.get("status", "")

            if t_title not in topic_stats:
                topic_stats[t_title] = {"attempts": 0, "solved": 0, "easy_solved": 0, "medium_solved": 0, "hard_solved": 0}

            topic_stats[t_title]["attempts"] += 1
            if st in ["Accepted", "Passed", "Success"]:
                topic_stats[t_title]["solved"] += 1
                if diff == "Easy":
                    topic_stats[t_title]["easy_solved"] += 1
                elif diff == "Medium":
                    topic_stats[t_title]["medium_solved"] += 1
                elif diff == "Hard":
                    topic_stats[t_title]["hard_solved"] += 1

        # Determine Topic Strength Matrix
        topic_matrix = {}
        for t_name, stats in topic_stats.items():
            att = stats["attempts"]
            sol = stats["solved"]
            acc = round((sol / max(1, att)) * 100, 1) if att > 0 else (100.0 if sol > 0 else 50.0)
            topic_matrix[t_name] = {
                "attempts": att,
                "solved": sol,
                "accuracy_pct": acc,
                "mastery": "High" if acc >= 75 and sol >= 2 else ("Medium" if acc >= 50 else "Low")
            }

        # Identify Weakest Topic
        weakest_topic = None
        min_acc = 999.0
        for t_name, m in topic_matrix.items():
            if m["accuracy_pct"] < min_acc:
                min_acc = m["accuracy_pct"]
                weakest_topic = t_name

        if not weakest_topic:
            weakest_topic = "Arrays"

        # Determine Difficulty Stage based on performance
        diff_stats = progress.get("difficultyStats", {})
        easy_history = sum(ts.get("easy_solved", 0) for ts in topic_stats.values())
        med_history = sum(ts.get("medium_solved", 0) for ts in topic_stats.values())

        easy_s = max(diff_stats.get("easy", {}).get("solved", 0), easy_history)
        med_s = max(diff_stats.get("medium", {}).get("solved", 0), med_history)
        overall_s = progress.get("overallSolved", 0)

        if med_s >= 2:
            target_difficulty = "Hard"
        elif overall_s >= 2 or med_s >= 1 or easy_s >= 2:
            target_difficulty = "Medium"
        else:
            target_difficulty = "Easy"

        return {
            "user_id": user_id_str,
            "solved_set": solved_set,
            "attempted_set": attempted_set,
            "recent_attempts": recent_attempts,
            "topic_matrix": topic_matrix,
            "weakest_topic": weakest_topic,
            "target_difficulty": target_difficulty,
            "overall_solved": len(solved_set)
        }

    @classmethod
    async def get_next_adaptive_problem(
        cls,
        user_id: str,
        topic_filter: Optional[str] = None,
        difficulty_filter: Optional[str] = None,
        role_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        profile = await cls.get_user_coding_profile(user_id)
        all_problems = coding_repository.get_all_seed_problems()

        solved_set = profile["solved_set"]
        recent_attempts = profile["recent_attempts"]
        weak_topic = topic_filter or profile["weakest_topic"]
        target_diff = difficulty_filter or profile["target_difficulty"]

        # Filter un-solved & non-recent candidate problems
        candidates = []
        for p in all_problems:
            pid = p["id"]
            if pid in solved_set:
                continue
            if pid in recent_attempts[:3]: # Skip recent 3 to avoid instant duplicate repeat
                continue

            c_topic = p.get("topic_title", p.get("category_title", ""))
            c_diff = p.get("difficulty", "Medium")

            # Role filter check if provided
            if role_filter:
                p_cat = p.get("category_title", "")
                if "Frontend" in role_filter and "System" in p_cat:
                    continue

            match_score = 0
            if weak_topic.lower() in c_topic.lower() or c_topic.lower() in weak_topic.lower():
                match_score += 50
            if c_diff.lower() == target_diff.lower():
                match_score += 30
            elif c_diff.lower() == "easy":
                match_score += 15

            candidates.append((match_score, p))

        # Sort candidate problems by match score descending
        candidates.sort(key=lambda x: x[0], reverse=True)

        if candidates:
            selected_problem = candidates[0][1]
            rationale = (
                f"Selected for your target area '{selected_problem.get('topic_title', 'DSA')}' "
                f"at {selected_problem.get('difficulty')} level based on your adaptive accuracy profile."
            )
        else:
            # Fallback if all solved
            selected_problem = all_problems[0]
            rationale = "Review challenge from core DSA topics."

        sanitized_p = sanitize_problem(selected_problem)

        # Challenge of the Day
        day_challenge = cls._get_challenge_of_the_day(all_problems, solved_set, profile["weakest_topic"])

        return {
            "status": "success",
            "user_id": str(user_id),
            "target_difficulty": target_diff,
            "focus_topic": weak_topic,
            "rationale": rationale,
            "next_problem": sanitized_p,
            "challenge_of_the_day": day_challenge
        }

    @classmethod
    def _get_challenge_of_the_day(
        cls,
        all_problems: List[Dict[str, Any]],
        solved_set: set,
        weak_topic: str
    ) -> Dict[str, Any]:
        for p in all_problems:
            if p["id"] not in solved_set and weak_topic.lower() in p.get("topic_title", "").lower():
                res = sanitize_problem(p)
                res["challenge_badge"] = f"DAILY CHALLENGE: {weak_topic.upper()}"
                return res

        for p in all_problems:
            if p["id"] not in solved_set:
                res = sanitize_problem(p)
                res["challenge_badge"] = "DAILY CHALLENGE: PROBLEM SOLVING"
                return res

        res = sanitize_problem(all_problems[0])
        res["challenge_badge"] = "DAILY CHALLENGE: FEATURED"
        return res

    @classmethod
    async def get_adaptive_queue(
        cls,
        user_id: str,
        limit: int = 6,
        topic_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        profile = await cls.get_user_coding_profile(user_id)
        all_problems = coding_repository.get_all_seed_problems()

        solved_set = profile["solved_set"]
        focus_topic = topic_filter or profile["weakest_topic"]

        # Build progressive ladder: Easy -> Medium -> Hard
        unsolved = [p for p in all_problems if p["id"] not in solved_set]
        if not unsolved:
            unsolved = all_problems

        # Topic matches first, ordered Easy -> Medium -> Hard
        topic_matched = [p for p in unsolved if focus_topic.lower() in p.get("topic_title", "").lower()]
        other_problems = [p for p in unsolved if p not in topic_matched]

        def diff_rank(p):
            d = p.get("difficulty", "Medium")
            return 1 if d == "Easy" else (2 if d == "Medium" else 3)

        topic_matched.sort(key=diff_rank)
        other_problems.sort(key=diff_rank)

        queue_problems = (topic_matched + other_problems)[:limit]
        result_queue = []

        for idx, p in enumerate(queue_problems):
            sp = sanitize_problem(p)
            sp["adaptive_step"] = idx + 1
            sp["ladder_level"] = f"Step {idx + 1}: {sp.get('difficulty')} {sp.get('topic_title', 'Topic')}"
            result_queue.append(sp)

        return result_queue

    @classmethod
    async def on_submission_evaluated(cls, user_id: str, problem_id: str, status: str) -> Dict[str, Any]:
        user_id_str = str(user_id)
        
        # 1. Update coding progress
        p_seed, top_doc, cat_doc = coding_repository.find_problem_in_seed(problem_id)
        if p_seed:
            await coding_repository.update_arena_progress(user_id_str, problem_id, top_doc.get("id", ""), 5)

        # 2. Trigger side-effect updates to Weakness Detector and Job Readiness
        try:
            from app.services.weakness_detector_service import WeaknessDetectorService
            await WeaknessDetectorService.analyze_user_weaknesses(user_id_str)
        except Exception:
            pass

        try:
            from app.services.job_readiness_service import JobReadinessService
            await JobReadinessService.compute_user_readiness(user_id_str)
        except Exception:
            pass

        return {"status": "success", "user_id": user_id_str, "problem_id": problem_id, "updated": True}
