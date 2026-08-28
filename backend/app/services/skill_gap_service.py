from typing import Dict, Any, List

BENCHMARK_SKILLS = {
    "Full Stack Developer": {
        "required": ["React", "Node.js", "Express", "MongoDB", "JavaScript", "TypeScript", "REST APIs", "Git", "Docker", "SQL", "Tailwind CSS"],
        "critical_weight": 0.6
    },
    "AI/ML Engineer": {
        "required": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "FastAPI", "Pandas", "NumPy", "Docker", "Data Structures", "MLOps"],
        "critical_weight": 0.7
    }
}

class SkillGapService:
    @staticmethod
    def analyze_gap(user_skills: List[str], target_role: str = "Full Stack Developer") -> Dict[str, Any]:
        role_data = BENCHMARK_SKILLS.get(target_role, BENCHMARK_SKILLS["Full Stack Developer"])
        required = role_data["required"]
        
        user_skills_clean = [s.strip().lower() for s in user_skills]
        
        acquired = [r for r in required if r.lower() in user_skills_clean]
        missing = [r for r in required if r.lower() not in user_skills_clean]
        
        readiness_pct = round((len(acquired) / len(required)) * 100) if required else 0
        
        return {
            "target_role": target_role,
            "readiness_percentage": readiness_pct,
            "total_required_skills": len(required),
            "acquired_skills": acquired,
            "missing_skills": missing,
            "estimated_learning_hours": len(missing) * 15,
            "next_highest_value_skill": missing[0] if missing else "None (Ready!)"
        }
