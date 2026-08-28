from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime, timedelta
from app.repositories.study_planner_repository import study_planner_repository
from app.services.weakness_detector_service import WeaknessDetectorService
from app.services.job_readiness_service import JobReadinessService

class StudyPlannerService:

    @classmethod
    async def generate_study_plan(cls, user_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        user_id_str = str(user_id)

        target_role = config.get("target_role", "Software Engineer")
        target_company = config.get("target_company")
        interview_date = config.get("interview_date")
        available_hours = int(config.get("available_hours_per_day", 2))
        days_per_week = int(config.get("days_per_week", 5))
        preferred_study_time = config.get("preferred_study_time", "Evening")
        skill_level = config.get("current_skill_level", "Intermediate")

        # Gather real platform weaknesses
        weakness_res = await WeaknessDetectorService.analyze_user_weaknesses(user_id_str)
        weaknesses = weakness_res.get("weaknesses", {})

        weak_dsa = weaknesses.get("weakest_dsa_topic", {}).get("name", "Trees")
        weak_tech = weaknesses.get("weakest_technical_skill", {}).get("name", "SQL")
        weak_interview = weaknesses.get("weakest_interview_dimension", {}).get("name", "Behavioral STAR")

        # Target interview date countdown calculation
        days_remaining = None
        is_accelerated = False
        if interview_date:
            try:
                target_dt = datetime.fromisoformat(interview_date.replace("Z", ""))
                days_remaining = max(1, (target_dt - datetime.utcnow()).days)
                if days_remaining <= 14:
                    is_accelerated = True
            except Exception:
                pass

        # Build 7-day template
        daily_minutes_budget = available_hours * 60
        days_schedule = []

        task_templates = [
            # Day 1
            {
                "day_number": 1,
                "day_name": "Day 1 - Core Problem Solving",
                "tasks": [
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": f"Practice {weak_dsa} DSA Problems",
                        "category": "DSA",
                        "duration_minutes": min(60, daily_minutes_budget),
                        "route": f"/coding-arena?topic={weak_dsa}",
                        "status": "pending"
                    },
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": f"Complete {weak_tech} Database Queries",
                        "category": "SQL",
                        "duration_minutes": min(30, max(20, daily_minutes_budget - 60)),
                        "route": "/coding-arena?category=SQL",
                        "status": "pending"
                    },
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": "Practice 5-Min Communication Delivery",
                        "category": "Prosody",
                        "duration_minutes": 20,
                        "route": "/gd-simulator",
                        "status": "pending"
                    }
                ]
            },
            # Day 2
            {
                "day_number": 2,
                "day_name": "Day 2 - Technical Depth & Resume Optimization",
                "tasks": [
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": "Solve 2 Medium Coding Arena Challenges",
                        "category": "DSA",
                        "duration_minutes": min(60, daily_minutes_budget),
                        "route": "/coding-arena",
                        "status": "pending"
                    },
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": "Optimize ATS Resume Bullet Points & Projects",
                        "category": "Resume",
                        "duration_minutes": 30,
                        "route": "/resume-analyzer",
                        "status": "pending"
                    }
                ]
            },
            # Day 3
            {
                "day_number": 3,
                "day_name": "Day 3 - AI Mock Interview Round",
                "tasks": [
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": f"Complete Mock Interview for {target_role}",
                        "category": "Interview",
                        "duration_minutes": 45,
                        "route": "/interview-simulator",
                        "status": "pending"
                    },
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": "Review Speech Delivery & Filler Words",
                        "category": "Prosody",
                        "duration_minutes": 20,
                        "route": "/speech-analyzer",
                        "status": "pending"
                    }
                ]
            },
            # Day 4
            {
                "day_number": 4,
                "day_name": "Day 4 - System Design & Fundamentals",
                "tasks": [
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": "System Design Architecture Evaluation",
                        "category": "System Design",
                        "duration_minutes": 45,
                        "route": "/roadmap",
                        "status": "pending"
                    },
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": f"Company Specific Prep for {target_company or 'Top Tech Tier 1'}",
                        "category": "Company Prep",
                        "duration_minutes": 30,
                        "route": "/company-prep",
                        "status": "pending"
                    }
                ]
            },
            # Day 5
            {
                "day_number": 5,
                "day_name": "Day 5 - Full Readiness Assessment",
                "tasks": [
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": "Mock OA Exam Simulation",
                        "category": "OA",
                        "duration_minutes": 60,
                        "route": "/oa-simulator",
                        "status": "pending"
                    },
                    {
                        "task_id": str(uuid.uuid4()),
                        "title": "Check AI Weakness Detector Progress",
                        "category": "Weakness",
                        "duration_minutes": 20,
                        "route": "/weakness-detector",
                        "status": "pending"
                    }
                ]
            }
        ]

        total_tasks = sum(len(d["tasks"]) for d in task_templates)

        plan_data = {
            "target_role": target_role,
            "target_company": target_company,
            "interview_date": interview_date,
            "days_remaining": days_remaining,
            "is_accelerated": is_accelerated,
            "available_hours_per_day": available_hours,
            "days_per_week": days_per_week,
            "preferred_study_time": preferred_study_time,
            "current_skill_level": skill_level,
            "days_schedule": task_templates,
            "total_tasks_count": total_tasks,
            "completed_tasks_count": 0,
            "completion_percentage": 0.0,
            "current_focus": f"DSA ({weak_dsa}) & {target_role} Interview Readiness"
        }

        return await study_planner_repository.save_user_plan(user_id_str, plan_data)

    @classmethod
    async def get_user_study_plan(cls, user_id: str) -> Dict[str, Any]:
        user_id_str = str(user_id)
        plan = await study_planner_repository.get_user_plan(user_id_str)
        if not plan:
            # Generate default plan
            plan = await cls.generate_study_plan(user_id_str, {
                "target_role": "Software Engineer",
                "available_hours_per_day": 2,
                "days_per_week": 5
            })
        return plan

    @classmethod
    async def complete_task(cls, user_id: str, task_id: str) -> Dict[str, Any]:
        user_id_str = str(user_id)
        plan = await study_planner_repository.get_user_plan(user_id_str)
        if not plan:
            return {"status": "error", "message": "Study plan not found"}

        task_found = False
        completed_count = 0
        total_count = 0

        for day in plan.get("days_schedule", []):
            for t in day.get("tasks", []):
                total_count += 1
                if t.get("task_id") == task_id:
                    t["status"] = "completed"
                    task_found = True
                if t.get("status") == "completed":
                    completed_count += 1

        if task_found:
            completion_pct = round((completed_count / max(1, total_count)) * 100, 1)
            plan["completed_tasks_count"] = completed_count
            plan["total_tasks_count"] = total_count
            plan["completion_percentage"] = completion_pct

            await study_planner_repository.save_user_plan(user_id_str, plan)
            
            # Side-effect: Recalculate Job Readiness Index
            try:
                await JobReadinessService.compute_user_readiness(user_id_str)
            except Exception:
                pass

        return {
            "status": "success",
            "task_id": task_id,
            "completion_percentage": plan.get("completion_percentage", 0),
            "completed_tasks_count": plan.get("completed_tasks_count", 0)
        }

    @classmethod
    async def reschedule_missed_tasks(cls, user_id: str) -> Dict[str, Any]:
        user_id_str = str(user_id)
        plan = await study_planner_repository.get_user_plan(user_id_str)
        if not plan:
            return {"status": "error", "message": "No active study plan"}

        rescheduled_count = 0
        days_schedule = plan.get("days_schedule", [])

        # Find pending tasks from Day 1 and Day 2 and reschedule to later days
        for idx, day in enumerate(days_schedule):
            if idx < 2:
                for t in day.get("tasks", []):
                    if t.get("status") == "pending":
                        t["status"] = "rescheduled"
                        # Append to next available day
                        if idx + 1 < len(days_schedule):
                            new_task = dict(t)
                            new_task["task_id"] = str(uuid.uuid4())
                            new_task["status"] = "pending"
                            new_task["title"] = f"[Rescheduled] {t.get('title')}"
                            days_schedule[idx + 1]["tasks"].append(new_task)
                            rescheduled_count += 1

        plan["days_schedule"] = days_schedule
        await study_planner_repository.save_user_plan(user_id_str, plan)

        return {
            "status": "success",
            "rescheduled_count": rescheduled_count,
            "plan": plan
        }
