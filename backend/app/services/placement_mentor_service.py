from typing import Dict, Any, List, Optional
import json
import asyncio
from datetime import datetime

from app.utils.gemini_client import gemini_client
from app.repositories.resume_repository import resume_repository
from app.repositories.coding_repository import coding_repository
from app.repositories.interview_repository import interview_repository
from app.repositories.gd_repository import gd_repository
from app.services.adaptive_coding_engine import AdaptiveCodingEngine
from app.services.job_readiness_service import JobReadinessService
from app.services.weakness_detector_service import WeaknessDetectorService
from app.services.job_matching_service import JobMatchingService
from app.repositories.application_repository import application_repository as applications_repository

class PlacementMentorService:

    @classmethod
    async def gather_user_mentor_context(cls, user_id: str) -> Dict[str, Any]:
        user_id_str = str(user_id)

        # 1. Resume & ATS Data
        resume_data = {}
        try:
            latest_resume = await resume_repository.get_latest_resume(user_id_str)
            if latest_resume:
                resume_data = {
                    "ats_score": latest_resume.get("ats_score") or latest_resume.get("overall_score", 0),
                    "section_scores": latest_resume.get("section_scores", {}),
                    "missing_skills": latest_resume.get("missing_skills", []),
                    "target_role": latest_resume.get("target_role", "Software Engineer")
                }
        except Exception:
            pass

        # 2. Coding Arena & Adaptive Data
        coding_data = {}
        try:
            coding_profile = await AdaptiveCodingEngine.get_user_coding_profile(user_id_str)
            progress = await coding_repository.get_user_arena_progress(user_id_str)
            coding_data = {
                "overall_solved": progress.get("overallSolved", 0),
                "target_difficulty": coding_profile.get("target_difficulty", "Easy"),
                "weak_dsa_topic": coding_profile.get("weakest_topic", "Arrays"),
                "topic_matrix": coding_profile.get("topic_matrix", {})
            }
        except Exception:
            pass

        # 3. Mock Interview Data
        interview_data = {}
        try:
            sessions = await interview_repository.get_user_sessions(user_id_str, limit=5)
            if sessions:
                scores = [s.get("overall_score", 0) for s in sessions if s.get("overall_score") is not None]
                avg_score = round(sum(scores) / max(1, len(scores)), 1) if scores else 0
                interview_data = {
                    "total_interviews": len(sessions),
                    "average_score": avg_score,
                    "latest_score": sessions[0].get("overall_score", 0)
                }
        except Exception:
            pass

        # 4. Group Discussion & Speech Data
        gd_data = {}
        try:
            gd_sessions = await gd_repository.get_user_history(user_id_str, limit=5)
            if gd_sessions:
                gd_scores = [g.get("gd_score", 0) for g in gd_sessions if g.get("gd_score") is not None]
                gd_data = {
                    "total_gd_sessions": len(gd_sessions),
                    "average_gd_score": round(sum(gd_scores) / max(1, len(gd_scores)), 1),
                    "latest_gd_score": gd_sessions[0].get("gd_score", 0)
                }
        except Exception:
            pass

        # 5. Job Readiness Data
        readiness_data = {}
        try:
            readiness_res = await JobReadinessService.compute_user_readiness(user_id_str)
            readiness_data = {
                "overall_readiness_score": readiness_res.get("overall_score", 0),
                "readiness_category": readiness_res.get("category", "Developing"),
                "pillar_scores": readiness_res.get("pillar_scores", {})
            }
        except Exception:
            pass

        # 6. AI Weakness Detector Data
        weakness_data = {}
        try:
            weakness_res = await WeaknessDetectorService.analyze_user_weaknesses(user_id_str)
            weaknesses = weakness_res.get("weaknesses", {})
            weakness_data = {
                "weakest_technical_skill": weaknesses.get("weakest_technical_skill", {}).get("name", "N/A"),
                "weakest_dsa_topic": weaknesses.get("weakest_dsa_topic", {}).get("name", "N/A"),
                "weakest_interview_dimension": weaknesses.get("weakest_interview_dimension", {}).get("name", "N/A"),
                "weakest_resume_section": weaknesses.get("weakest_resume_section", {}).get("name", "N/A")
            }
        except Exception:
            pass

        # 7. Job Application Pipeline
        app_data = {}
        try:
            apps = await applications_repository.get_user_applications(user_id_str)
            app_data = {
                "total_applications": len(apps),
                "interview_stage_count": sum(1 for a in apps if a.get("status") in ["Interviewing", "Offer"])
            }
        except Exception:
            pass

        # Data availability flags
        has_resume = bool(resume_data and resume_data.get("ats_score", 0) > 0)
        has_coding = bool(coding_data and coding_data.get("overall_solved", 0) > 0)
        has_interview = bool(interview_data and interview_data.get("total_interviews", 0) > 0)
        has_gd = bool(gd_data and gd_data.get("total_gd_sessions", 0) > 0)

        context = {
            "user_id": user_id_str,
            "has_resume_data": has_resume,
            "has_coding_data": has_coding,
            "has_interview_data": has_interview,
            "has_gd_data": has_gd,
            "resume": resume_data,
            "coding": coding_data,
            "interview": interview_data,
            "group_discussion": gd_data,
            "job_readiness": readiness_data,
            "weaknesses": weakness_data,
            "applications": app_data
        }

        return context

    @classmethod
    def _extract_recommendations(cls, message_lower: str, context: Dict[str, Any]) -> List[Dict[str, str]]:
        recs = []

        if any(k in message_lower for k in ["coding", "dsa", "tree", "array", "graph", "problem", "practice"]):
            weak_topic = context.get("coding", {}).get("weak_dsa_topic", "DSA Topics")
            recs.append({
                "label": f"Practice {weak_topic} in Coding Arena",
                "route": "/coding-arena"
            })

        if any(k in message_lower for k in ["interview", "ready", "mock", "behavioral"]):
            recs.append({
                "label": "Take AI Mock Technical Interview",
                "route": "/interview-simulator"
            })

        if any(k in message_lower for k in ["resume", "ats", "score", "project", "bullet"]):
            recs.append({
                "label": "Analyze & Boost Resume Score",
                "route": "/resume-analyzer"
            })

        if any(k in message_lower for k in ["speak", "gd", "discussion", "communication"]):
            recs.append({
                "label": "Practice 5-Min AI Group Discussion",
                "route": "/gd-simulator"
            })

        if any(k in message_lower for k in ["job", "match", "hiring", "apply"]):
            recs.append({
                "label": "View Matched Jobs for Your Skillset",
                "route": "/job-matcher"
            })

        if not recs:
            recs = [
                {"label": "Solve Coding Challenge", "route": "/coding-arena"},
                {"label": "Check AI Weakness Detector", "route": "/weakness-detector"},
                {"label": "Run ATS Resume Optimizer", "route": "/resume-analyzer"}
            ]

        return recs[:3]

    @classmethod
    async def generate_mentor_response(
        cls,
        user_id: str,
        user_message: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        user_id_str = str(user_id)
        msg_raw = user_message.strip()
        msg_lower = msg_raw.lower()

        # Gather real platform context
        ctx = await cls.gather_user_mentor_context(user_id_str)

        # Build prompt for Gemini
        system_prompt = f"""
You are Antigravity AI Placement Mentor, an empathetic, highly structured, expert technical career mentor.
You are pair-programming and mentoring candidate (User ID: {user_id_str}).

Candidate Platform Performance Context (GROUND TRUTH DATA):
{json.dumps(ctx, indent=2)}

STRICT RULES:
1. Base your answer strictly on the candidate's actual platform metrics listed above.
2. If the user asks about an area where the relevant data is missing or zero (e.g. asking about interview readiness when has_interview_data is false, or asking about resume score when has_resume_data is false), YOU MUST SAY:
   "I don't have enough data to evaluate that yet." then recommend the exact module to complete.
3. DO NOT fabricate metrics, numbers, or claim the user completed interviews/scans if the context shows 0.
4. Keep responses encouraging, structured (use Markdown bullet points), actionable, and concise.
5. NEVER expose passwords, API keys, JWT tokens, internal database URIs, or another user's data.
"""

        prompt = f"{system_prompt}\nUser Question: {msg_raw}"

        reply = ""
        try:
            gemini_res = await gemini_client.generate_text(prompt)
            if gemini_res and len(gemini_res.strip()) > 15:
                reply = gemini_res.strip()
        except Exception:
            pass

        # Fallback Engine if Gemini is offline or failed
        if not reply:
            if "ready" in msg_lower or "interview" in msg_lower:
                if not ctx.get("has_interview_data") and not ctx.get("has_coding_data"):
                    reply = "I don't have enough data to evaluate that yet. Complete at least one Mock Interview and a Coding Challenge to generate your readiness analysis."
                else:
                    readiness = ctx.get("job_readiness", {}).get("overall_readiness_score", 65)
                    ats = ctx.get("resume", {}).get("ats_score", 0)
                    solved = ctx.get("coding", {}).get("overall_solved", 0)
                    reply = f"Based on your actual platform performance:\n- Job Readiness Index: **{readiness}/100**\n- ATS Resume Score: **{ats}%**\n- Coding Problems Solved: **{solved}**\n\nTo reach top-tier interview readiness, aim for an ATS score above 85% and complete 2 more mock interviews."
            elif "weakness" in msg_lower or "weak" in msg_lower:
                w = ctx.get("weaknesses", {})
                if w.get("weakest_technical_skill") == "N/A":
                    reply = "I don't have enough data to evaluate that yet. Take a coding test or resume scan to identify your top weaknesses."
                else:
                    reply = f"Here are your identified areas for growth:\n- Weakest Technical Skill: **{w.get('weakest_technical_skill')}**\n- Weakest DSA Topic: **{w.get('weakest_dsa_topic')}**\n- Weakest Interview Area: **{w.get('weakest_interview_dimension')}**"
            elif "study" in msg_lower or "practice" in msg_lower or "coding" in msg_lower:
                target_diff = ctx.get("coding", {}).get("target_difficulty", "Medium")
                weak_dsa = ctx.get("coding", {}).get("weak_dsa_topic", "Trees")
                reply = f"Today's recommended practice plan:\n1. Solve 2 **{target_diff}** problems in **{weak_dsa}** in the Coding Arena.\n2. Review your resume section scores.\n3. Conduct a 5-minute Group Discussion session."
            elif "job" in msg_lower or "match" in msg_lower:
                target_role = ctx.get("resume", {}).get("target_role", "Software Engineer")
                reply = f"Your current profile aligns best with **{target_role}** roles. Top hiring partners include Google, Amazon, IBM, and Swiggy."
            elif "resume" in msg_lower or "ats" in msg_lower:
                ats = ctx.get("resume", {}).get("ats_score", 0)
                if ats == 0:
                    reply = "I don't have enough data to evaluate that yet. Upload your resume to the ATS Resume Scorer to view keyword and section recommendations."
                else:
                    reply = f"Your current ATS score is **{ats}%**. Focus on adding quantifiable project metrics and filling missing technical skills."
            else:
                readiness = ctx.get("job_readiness", {}).get("overall_readiness_score", 70)
                reply = f"As your Placement Mentor, I'm tracking your progress across all platform modules. Your current Job Readiness Index is **{readiness}/100**. Ask me any question about your interview readiness, resume score, or coding topics!"

        actionable_recommendations = cls._extract_recommendations(msg_lower, ctx)

        return {
            "status": "success",
            "reply": reply,
            "context_summary": {
                "ats_score": ctx.get("resume", {}).get("ats_score", 0),
                "job_readiness_score": ctx.get("job_readiness", {}).get("overall_readiness_score", 0),
                "coding_solved": ctx.get("coding", {}).get("overall_solved", 0),
                "weakest_dsa_topic": ctx.get("coding", {}).get("weak_dsa_topic", "Arrays")
            },
            "actionable_recommendations": actionable_recommendations
        }
