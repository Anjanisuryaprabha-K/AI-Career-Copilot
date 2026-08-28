from typing import Dict, Any, List, Optional
from datetime import datetime
from app.repositories.skill_radar_repository import skill_radar_repository
from app.repositories.resume_repository import resume_repository
from app.repositories.coding_repository import coding_repository
from app.repositories.interview_repository import interview_repository
from app.repositories.gd_repository import gd_repository

ROLE_TARGET_BENCHMARKS: Dict[str, Dict[str, int]] = {
    "Software Engineer": {
        "DSA": 85,
        "Programming": 85,
        "SQL": 75,
        "Database": 70,
        "Frontend": 65,
        "Backend": 75,
        "System Design": 70,
        "Cloud/DevOps": 60,
        "Communication": 75,
        "Interview": 80,
        "Resume": 85,
        "Problem Solving": 80
    },
    "Full Stack Developer": {
        "DSA": 80,
        "Programming": 85,
        "SQL": 80,
        "Database": 75,
        "Frontend": 85,
        "Backend": 85,
        "System Design": 75,
        "Cloud/DevOps": 70,
        "Communication": 75,
        "Interview": 80,
        "Resume": 85,
        "Problem Solving": 80
    },
    "Frontend Developer": {
        "DSA": 70,
        "Programming": 85,
        "SQL": 60,
        "Database": 55,
        "Frontend": 90,
        "Backend": 60,
        "System Design": 65,
        "Cloud/DevOps": 55,
        "Communication": 75,
        "Interview": 80,
        "Resume": 85,
        "Problem Solving": 75
    },
    "Backend Developer": {
        "DSA": 85,
        "Programming": 85,
        "SQL": 85,
        "Database": 85,
        "Frontend": 55,
        "Backend": 90,
        "System Design": 80,
        "Cloud/DevOps": 75,
        "Communication": 75,
        "Interview": 80,
        "Resume": 85,
        "Problem Solving": 80
    },
    "Data Engineer": {
        "DSA": 80,
        "Programming": 85,
        "SQL": 95,
        "Database": 90,
        "Frontend": 45,
        "Backend": 80,
        "System Design": 80,
        "Cloud/DevOps": 80,
        "Communication": 70,
        "Interview": 80,
        "Resume": 85,
        "Problem Solving": 85
    },
    "Data Scientist": {
        "DSA": 75,
        "Programming": 85,
        "SQL": 85,
        "Database": 80,
        "Frontend": 50,
        "Backend": 65,
        "System Design": 65,
        "Cloud/DevOps": 60,
        "Communication": 75,
        "Interview": 80,
        "Resume": 85,
        "Problem Solving": 85
    }
}

class SkillRadarService:

    @classmethod
    async def compute_skill_radar(cls, user_id: str, target_role: str = "Software Engineer") -> Dict[str, Any]:
        user_id_str = str(user_id)
        benchmarks = ROLE_TARGET_BENCHMARKS.get(target_role, ROLE_TARGET_BENCHMARKS["Software Engineer"])

        # 1. Fetch Resume Data
        latest_resume = await resume_repository.get_latest_resume(user_id_str)
        ats_score = (latest_resume.get("ats_score") or latest_resume.get("overall_score")) if latest_resume else None
        section_scores = latest_resume.get("section_scores", {}) if latest_resume else {}

        # 2. Fetch Coding Data
        progress = await coding_repository.get_user_arena_progress(user_id_str)
        solved_count = progress.get("overallSolved", 0)
        attempts = progress.get("totalAttempts", 0)
        accuracy = progress.get("overallAccuracy", 0)

        # 3. Fetch Interview Data
        sessions = await interview_repository.get_user_sessions(user_id_str, limit=5)
        interview_scores = [s.get("overall_score", 0) for s in sessions if s.get("overall_score") is not None]
        avg_interview = round(sum(interview_scores) / max(1, len(interview_scores)), 1) if interview_scores else None

        # 4. Fetch GD Data
        gd_sessions = await gd_repository.get_user_history(user_id_str, limit=5)
        gd_scores = [g.get("gd_score", 0) for g in gd_sessions if g.get("gd_score") is not None]
        avg_gd = round(sum(gd_scores) / max(1, len(gd_scores)), 1) if gd_scores else None

        # Calculate 12 empirical axes
        axes: Dict[str, Dict[str, Any]] = {}

        # Axis 1: DSA
        if attempts > 0:
            dsa_val = min(100, round((solved_count * 5) + (accuracy * 0.4)))
            axes["DSA"] = {"score": dsa_val, "status": "evaluated"}
        else:
            axes["DSA"] = {"score": None, "status": "not_enough_data"}

        # Axis 2: Programming
        if attempts > 0:
            prog_val = min(100, round(50 + (solved_count * 4)))
            axes["Programming"] = {"score": prog_val, "status": "evaluated"}
        else:
            axes["Programming"] = {"score": None, "status": "not_enough_data"}

        # Axis 3: SQL
        all_solved_ids = set((progress.get("completedProblems") or []) + (progress.get("solvedIds") or []))
        sql_solved = sum(1 for p in all_solved_ids if "sql" in p.lower() or "db" in p.lower())
        if sql_solved == 0:
            history = await coding_repository.get_user_history(user_id_str)
            sql_solved = sum(1 for att in history if att.get("language") == "sql" or "sql" in str(att.get("problem_id", "")).lower())
        if sql_solved > 0:
            axes["SQL"] = {"score": min(100, round(60 + (sql_solved * 10))), "status": "evaluated"}
        else:
            axes["SQL"] = {"score": None, "status": "not_enough_data"}

        # Axis 4: Database
        if sql_solved > 0:
            axes["Database"] = {"score": min(100, round(55 + (sql_solved * 8))), "status": "evaluated"}
        else:
            axes["Database"] = {"score": None, "status": "not_enough_data"}

        def _get_sec_score(val, default=70):
            if isinstance(val, (int, float)):
                return float(val)
            if isinstance(val, dict):
                return float(val.get("score", default))
            return float(default)

        # Axis 5: Frontend
        if section_scores.get("projects") or section_scores.get("skills"):
            fe_score_val = _get_sec_score(section_scores.get("projects"), 70)
            fe_val = min(100, round(fe_score_val * 0.9))
            axes["Frontend"] = {"score": fe_val, "status": "evaluated"}
        else:
            axes["Frontend"] = {"score": None, "status": "not_enough_data"}

        # Axis 6: Backend
        if attempts > 0 or ats_score is not None:
            be_val = min(100, round((ats_score or 65) * 0.85))
            axes["Backend"] = {"score": be_val, "status": "evaluated"}
        else:
            axes["Backend"] = {"score": None, "status": "not_enough_data"}

        # Axis 7: System Design
        if solved_count >= 5:
            axes["System Design"] = {"score": min(100, round(50 + (solved_count * 3))), "status": "evaluated"}
        else:
            axes["System Design"] = {"score": None, "status": "not_enough_data"}

        # Axis 8: Cloud/DevOps
        if section_scores.get("skills"):
            devops_score_val = _get_sec_score(section_scores.get("skills"), 60)
            axes["Cloud/DevOps"] = {"score": min(100, round(devops_score_val * 0.8)), "status": "evaluated"}
        else:
            axes["Cloud/DevOps"] = {"score": None, "status": "not_enough_data"}

        # Axis 9: Communication
        if avg_gd is not None:
            axes["Communication"] = {"score": round(avg_gd), "status": "evaluated"}
        else:
            axes["Communication"] = {"score": None, "status": "not_enough_data"}

        # Axis 10: Interview
        if avg_interview is not None:
            axes["Interview"] = {"score": round(avg_interview), "status": "evaluated"}
        else:
            axes["Interview"] = {"score": None, "status": "not_enough_data"}

        # Axis 11: Resume
        if ats_score is not None:
            axes["Resume"] = {"score": round(ats_score), "status": "evaluated"}
        else:
            axes["Resume"] = {"score": None, "status": "not_enough_data"}

        # Axis 12: Problem Solving
        if attempts > 0:
            ps_val = min(100, round((accuracy * 0.6) + (solved_count * 3)))
            axes["Problem Solving"] = {"score": ps_val, "status": "evaluated"}
        else:
            axes["Problem Solving"] = {"score": None, "status": "not_enough_data"}

        # Compute Skill Gaps against Benchmarks
        max_gap = -1
        highest_gap_axis = "DSA"
        recommended_route = "/coding-arena"
        recommended_action = "Practice 3 Medium DSA Challenges"

        evaluated_scores = []

        for axis, info in axes.items():
            sc = info["score"]
            if sc is not None:
                evaluated_scores.append(sc)
                target_benchmark = benchmarks.get(axis, 75)
                gap = target_benchmark - sc
                if gap > max_gap:
                    max_gap = gap
                    highest_gap_axis = axis

        # Route mapping for highest gap
        route_map = {
            "DSA": ("/coding-arena", "Practice DSA Problems in Coding Arena"),
            "Programming": ("/coding-arena", "Solve Language Coding Challenges"),
            "SQL": ("/coding-arena?category=SQL", "Complete SQL Query Exercises"),
            "Database": ("/coding-arena?category=SQL", "Practice Database Schema Design"),
            "Frontend": ("/roadmap", "Review Frontend Capstone Roadmap"),
            "Backend": ("/roadmap", "Review Backend Architecture Roadmap"),
            "System Design": ("/roadmap", "Complete System Design Module"),
            "Cloud/DevOps": ("/roadmap", "Study DevOps CI/CD Workflows"),
            "Communication": ("/gd-simulator", "Practice 5-Min Group Discussion"),
            "Interview": ("/interview-simulator", "Take Mock Technical Interview"),
            "Resume": ("/resume-analyzer", "Optimize Resume ATS Keyword Match"),
            "Problem Solving": ("/coding-arena", "Solve Hard Coding Problems")
        }

        if highest_gap_axis in route_map:
            recommended_route, recommended_action = route_map[highest_gap_axis]

        overall_avg = round(sum(evaluated_scores) / max(1, len(evaluated_scores)), 1) if evaluated_scores else 0

        snapshot = {
            "target_role": target_role,
            "evaluated_axes": axes,
            "target_benchmarks": benchmarks,
            "highest_gap": {
                "axis": highest_gap_axis,
                "gap_points": max(0, max_gap),
                "recommended_action": recommended_action,
                "route": recommended_route
            },
            "overall_average_score": overall_avg
        }

        await skill_radar_repository.save_snapshot(user_id_str, snapshot)

        return snapshot

    @classmethod
    async def get_radar_history(cls, user_id: str) -> List[Dict[str, Any]]:
        user_id_str = str(user_id)
        return await skill_radar_repository.get_history(user_id_str)
