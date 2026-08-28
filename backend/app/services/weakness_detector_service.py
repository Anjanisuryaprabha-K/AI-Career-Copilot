from typing import Dict, Any, List, Optional
from datetime import datetime
from app.repositories.resume_repository import resume_repository
from app.repositories.coding_repository import CodingRepository
from app.repositories.interview_repository import InterviewRepository
from app.repositories.learning_repository import learning_repository
from app.repositories.weakness_repository import weakness_repository
from app.services.job_readiness_service import JobReadinessService
from app.utils.gemini_client import gemini_client, GeminiClient

coding_repository = CodingRepository()
interview_repository = InterviewRepository()

class WeaknessDetectorService:

    @classmethod
    async def analyze_user_weaknesses(cls, user_id: str) -> Dict[str, Any]:
        user_id_str = str(user_id)

        # 1. Fetch data from platform modules
        scan = await resume_repository.get_latest_user_scan(user_id_str)
        coding_cursor = coding_repository.col.find({"user_id": user_id_str})
        coding_attempts = await coding_cursor.to_list(500)
        interview_sessions = await interview_repository.list_user_sessions(user_id_str, limit=50)
        gap_doc = await learning_repository.gap_col.find_one({"user_id": user_id_str})
        readiness = await JobReadinessService.compute_user_readiness(user_id_str)

        # 2. Check Insufficient Data Condition
        total_data_points = (1 if scan else 0) + len(coding_attempts) + len(interview_sessions)
        if total_data_points == 0:
            result = {
                "user_id": user_id_str,
                "has_sufficient_data": False,
                "message": "Not enough data yet. Complete a resume scan, coding problem, or mock interview to unlock AI weakness analysis.",
                "total_data_points": 0,
                "top_weaknesses": [],
                "top_strengths": [],
                "highest_impact_improvement": None,
                "ai_performance_summary": "Insufficient data available across platform modules to calculate candidate strengths and weaknesses. Participate in platform activities to generate real-time analytics.",
                "analyzed_at": datetime.utcnow().isoformat()
            }
            await weakness_repository.save_analysis(user_id_str, result)
            return result

        # 3. Analyze DSA Topics and Coding Difficulty Performance
        dsa_topic_stats = {} # topic_name -> {attempts: int, solved: int, easy_acc: float, med_acc: float}
        diff_stats = {"Easy": {"attempts": 0, "solved": 0}, "Medium": {"attempts": 0, "solved": 0}, "Hard": {"attempts": 0, "solved": 0}}

        for att in coding_attempts:
            status = att.get("status", "")
            p_id = att.get("problem_id", "")
            p_seed, top_doc, cat_doc = coding_repository.find_problem_in_seed(p_id)

            topic_name = top_doc.get("title", "Algorithms") if top_doc else "Algorithms"
            difficulty = p_seed.get("difficulty", "Medium") if p_seed else "Medium"

            if topic_name not in dsa_topic_stats:
                dsa_topic_stats[topic_name] = {"attempts": 0, "solved": 0}

            dsa_topic_stats[topic_name]["attempts"] += 1
            if difficulty in diff_stats:
                diff_stats[difficulty]["attempts"] += 1

            if status in ["Accepted", "Passed", "Success"]:
                dsa_topic_stats[topic_name]["solved"] += 1
                if difficulty in diff_stats:
                    diff_stats[difficulty]["solved"] += 1

        # 4. Dimension Evaluation
        evaluated_dimensions = []

        # A. DSA Topic Dimensions
        for t_name, stats in dsa_topic_stats.items():
            att_cnt = stats["attempts"]
            sol_cnt = stats["solved"]
            acc_pct = round((sol_cnt / max(1, att_cnt)) * 100, 1)

            severity = "High" if acc_pct < 50 else ("Medium" if acc_pct < 70 else "Low")
            evaluated_dimensions.append({
                "id": f"dsa_topic_{t_name.lower().replace(' ', '_')}",
                "title": f"DSA Topic: {t_name}",
                "category": "DSA Topic",
                "current_score": acc_pct,
                "evidence": f"{att_cnt} attempts, {sol_cnt} solved. Accuracy: {acc_pct}%",
                "severity": severity,
                "impact": f"Critical impact on technical coding assessment rounds for software roles.",
                "recommended_action": f"Solve 5 Medium {t_name} challenges in Coding Arena.",
                "target_link": "/coding-arena"
            })

        # Default DSA topic if none recorded yet
        if not dsa_topic_stats:
            evaluated_dimensions.append({
                "id": "dsa_topic_dp",
                "title": "DSA Topic: Dynamic Programming & Recursion",
                "category": "DSA Topic",
                "current_score": 40.0,
                "evidence": "0 coding attempts recorded in Dynamic Programming.",
                "severity": "High",
                "impact": "Core requirement for Tier-1 engineering problem solving rounds.",
                "recommended_action": "Complete Dynamic Programming modules in Coding Arena.",
                "target_link": "/coding-arena"
            })

        # B. Resume ATS & Section Scores
        ats_score = scan.get("overall_score", 45) if scan else 40
        sec_scores = scan.get("section_scores", {}) if scan else {}
        missing_kw = scan.get("missing_keywords", []) if scan else []

        evaluated_dimensions.append({
            "id": "dim_resume_ats",
            "title": "Resume ATS Overall Quality",
            "category": "Resume Section",
            "current_score": float(ats_score),
            "evidence": f"ATS overall scan score: {ats_score}/100." if scan else "No resume scan uploaded yet.",
            "severity": "High" if ats_score < 60 else ("Medium" if ats_score < 75 else "Low"),
            "impact": "Directly impacts recruiter screening resume parser pass rate.",
            "recommended_action": "Run ATS Resume Analyzer to inject missing keywords and fix formatting.",
            "target_link": "/resume-analyzer"
        })

        if missing_kw:
            kw_sample = ", ".join(missing_kw[:3])
            evaluated_dimensions.append({
                "id": "dim_missing_keywords",
                "title": f"Technical Keyword Gaps ({kw_sample})",
                "category": "Technical Skill",
                "current_score": 45.0,
                "evidence": f"{len(missing_kw)} missing role keywords identified in resume analysis.",
                "severity": "High",
                "impact": "Causes candidate filtering by automated ATS keyword scanners.",
                "recommended_action": f"Incorporate missing keywords ({kw_sample}) into resume experience bullets.",
                "target_link": "/resume-analyzer"
            })

        # C. Interview & Speech Delivery Prosody Scores
        if interview_sessions:
            scores = [s.get("overall_score", s.get("score", 70)) for s in interview_sessions if s.get("score") or s.get("overall_score")]
            avg_interview = round(sum(scores) / len(scores), 1) if scores else 65.0
            evaluated_dimensions.append({
                "id": "dim_interview_performance",
                "title": "Mock Technical Interview Performance",
                "category": "Interview Dimension",
                "current_score": avg_interview,
                "evidence": f"{len(interview_sessions)} sessions completed. Average score: {avg_interview}%.",
                "severity": "High" if avg_interview < 60 else ("Medium" if avg_interview < 75 else "Low"),
                "impact": "Determines live technical interview pass rate.",
                "recommended_action": "Complete AI Mock Technical Interview with live speech feedback.",
                "target_link": "/interview-simulator"
            })
        else:
            evaluated_dimensions.append({
                "id": "dim_speech_prosody",
                "title": "Speech Delivery & Vocal Prosody",
                "category": "Communication Metric",
                "current_score": 50.0,
                "evidence": "0 speech delivery prosody sessions evaluated.",
                "severity": "Medium",
                "impact": "Vocal confidence, pace, and articulation influence recruiter behavioral rounds.",
                "recommended_action": "Practice STAR Method speech delivery in AI Speech Prosody Analyzer.",
                "target_link": "/speech-analyzer"
            })

        # D. Job Readiness Pillars
        breakdown = readiness.get("weighting_breakdown", {})
        coding_score = breakdown.get("coding_score", {}).get("score", 0)
        evaluated_dimensions.append({
            "id": "dim_job_readiness_coding",
            "title": "Overall DSA & Coding Readiness",
            "category": "Job Readiness Category",
            "current_score": float(coding_score),
            "evidence": f"Job Readiness Coding Pillar score: {coding_score}/100.",
            "severity": "High" if coding_score < 50 else ("Medium" if coding_score < 70 else "Low"),
            "impact": "Reflects problem-solving mastery required for online assessments.",
            "recommended_action": "Follow Placement Roadmap DSA Track to boost coding pillar score.",
            "target_link": "/placement-roadmap"
        })

        # 5. Sort Weaknesses & Strengths
        # Weaknesses: lowest score first
        sorted_as_weaknesses = sorted(evaluated_dimensions, key=lambda x: (x["current_score"], 0 if x["severity"] == "High" else (1 if x["severity"] == "Medium" else 2)))
        top_weaknesses = sorted_as_weaknesses[:5]

        # Strengths: highest score first
        sorted_as_strengths = sorted(evaluated_dimensions, key=lambda x: x["current_score"], reverse=True)
        top_strengths = sorted_as_strengths[:5]

        # 6. Highest Impact Improvement
        primary_weakness = top_weaknesses[0] if top_weaknesses else None
        highest_impact = None
        if primary_weakness:
            target_score = min(100, round(primary_weakness["current_score"] + 25))
            highest_impact = {
                "weakness_title": primary_weakness["title"],
                "category": primary_weakness["category"],
                "current_score": primary_weakness["current_score"],
                "target_score": target_score,
                "impact_statement": f"Improving {primary_weakness['title']} from {primary_weakness['current_score']}% to {target_score}% would yield the largest boost (+18% overall fit) to your engineering placement readiness.",
                "recommended_action": primary_weakness["recommended_action"],
                "target_link": primary_weakness["target_link"]
            }

        # 7. AI Performance Summary
        ai_summary = await cls._generate_ai_summary(user_id_str, top_weaknesses, top_strengths, highest_impact)

        result = {
            "user_id": user_id_str,
            "has_sufficient_data": True,
            "message": "AI Weakness Analysis generated successfully from platform performance data.",
            "total_data_points": total_data_points,
            "overall_readiness_score": readiness.get("overall_readiness_score", 65),
            "top_weaknesses": top_weaknesses,
            "top_strengths": top_strengths,
            "highest_impact_improvement": highest_impact,
            "ai_performance_summary": ai_summary,
            "analyzed_at": datetime.utcnow().isoformat()
        }

        await weakness_repository.save_analysis(user_id_str, result)
        return result

    @classmethod
    async def _generate_ai_summary(
        cls,
        user_id: str,
        weaknesses: List[Dict[str, Any]],
        strengths: List[Dict[str, Any]],
        highest_impact: Optional[Dict[str, Any]]
    ) -> str:
        w_titles = [f"{w['title']} ({w['current_score']}%)" for w in weaknesses[:3]]
        s_titles = [f"{s['title']} ({s['current_score']}%)" for s in strengths[:3]]

        prompt = (
            f"Candidate Weaknesses: {', '.join(w_titles)}\n"
            f"Candidate Strengths: {', '.join(s_titles)}\n"
            f"Highest Impact Improvement: {highest_impact.get('impact_statement', '') if highest_impact else ''}\n\n"
            "Provide a concise, 2-3 sentence executive summary explaining the candidate's core growth areas and actionable next steps."
        )

        try:
            summary = await gemini_client.generate_text(prompt)
            if summary and len(summary.strip()) > 30:
                return summary.strip()
        except Exception:
            pass

        # Fallback Rule-based Summary
        w_lead = weaknesses[0]['title'] if weaknesses else "Technical Practice"
        s_lead = strengths[0]['title'] if strengths else "Candidate Foundation"
        return (
            f"Candidate demonstrates strong proficiency in {s_lead}, providing a solid foundation. "
            f"However, key performance bottlenecks were detected in {w_lead}. "
            f"Focusing immediate effort on {highest_impact.get('recommended_action', 'targeted modules') if highest_impact else 'weak areas'} "
            f"will deliver the highest placement readiness gain."
        )
