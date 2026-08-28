class MatchingService:
    @staticmethod
    def match_resume_to_jobs(skills: list, experience_level: str = "Student / Fresh Graduate") -> dict:
        user_skills_set = set([s.lower().strip() for s in skills])
        
        job_catalog = [
            {
                "company": "Amazon",
                "role": "SDE 1 (Software Development Engineer)",
                "required_skills": ["Data Structures", "Algorithms", "Python", "Java", "System Design", "AWS"],
                "ctc": "₹18 - 24 LPA",
                "match_reason": "High alignment in Algorithms, Backend, and Problem Solving."
            },
            {
                "company": "Swiggy",
                "role": "Software Engineer - Backend (FastAPI / Go)",
                "required_skills": ["Python", "FastAPI", "MongoDB", "Redis", "Distributed Systems", "Docker"],
                "ctc": "₹14 - 20 LPA",
                "match_reason": "Direct match for your Python, FastAPI, and MongoDB stack."
            },
            {
                "company": "Razorpay",
                "role": "Frontend Engineer (React / TypeScript)",
                "required_skills": ["React", "JavaScript", "TypeScript", "Tailwind CSS", "Redux", "REST APIs"],
                "ctc": "₹12 - 18 LPA",
                "match_reason": "Excellent match for modern frontend architecture and React proficiency."
            },
            {
                "company": "Microsoft",
                "role": "Full Stack Engineer (Azure Cloud)",
                "required_skills": ["TypeScript", "React", "Node.js", "C#", "SQL", "Cloud Architecture"],
                "ctc": "₹16 - 26 LPA",
                "match_reason": "Strong foundation for enterprise full-stack development."
            }
        ]
        
        matches = []
        for job in job_catalog:
            req_set = set([r.lower() for r in job["required_skills"]])
            matched_skills = [r for r in job["required_skills"] if r.lower() in user_skills_set]
            missing_skills = [r for r in job["required_skills"] if r.lower() not in user_skills_set]
            match_pct = round((len(matched_skills) / len(job["required_skills"])) * 100)
            
            matches.append({
                "company": job["company"],
                "role": job["role"],
                "ctc": job["ctc"],
                "match_percentage": max(45, match_pct),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "insights": job["match_reason"]
            })
            
        matches.sort(key=lambda x: x["match_percentage"], reverse=True)
        return {"matched_jobs": matches}
