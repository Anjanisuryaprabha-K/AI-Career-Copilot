import re
from typing import Dict, Any, List, Optional

class JobMatchingService:
    @staticmethod
    def extract_work_type(location: str, snippet: str = "") -> str:
        combined = f"{location} {snippet}".lower()
        if "remote" in combined:
            return "Remote"
        elif "hybrid" in combined:
            return "Hybrid"
        else:
            return "On-Site"

    @staticmethod
    def parse_salary_num(salary_str: str) -> float:
        match = re.search(r"(\d+)", salary_str)
        if match:
            return float(match.group(1))
        return 0.0

    @classmethod
    def calculate_job_match(
        cls,
        job: Dict[str, Any],
        user_skills: List[str],
        target_role: str,
        user_education: List[Dict[str, Any]] = None,
        user_experience: List[Dict[str, Any]] = None,
        user_projects: List[Dict[str, Any]] = None,
        experience_level: str = "Intermediate"
    ) -> Dict[str, Any]:
        user_skills_clean = list(dict.fromkeys([s.strip().lower() for s in user_skills if s.strip()]))
        user_skills_set = set(user_skills_clean)

        job_title = job.get("title", job.get("job_title", target_role))
        job_skills = job.get("skills", job.get("required_skills", ["Python", "React", "SQL"]))
        job_skills_clean = [s.strip() for s in job_skills]
        job_skills_lower = [s.lower() for s in job_skills_clean]
        job_skills_set = set(job_skills_lower)

        job_exp_req = job.get("experience", job.get("experience_required", "0-2 Years"))
        job_location = job.get("location", "India")
        job_salary = job.get("salary", "₹16 - ₹24 LPA")
        work_type = cls.extract_work_type(job_location, job.get("snippet", job.get("description", "")))

        # 1. SKILLS MATCH (35%)
        matching_skills = [job_skills_clean[i] for i, s in enumerate(job_skills_lower) if s in user_skills_set]
        missing_skills = [job_skills_clean[i] for i, s in enumerate(job_skills_lower) if s not in user_skills_set]
        
        overlap_count = len(matching_skills)
        total_req = max(1, len(job_skills_clean))
        skills_score = round((overlap_count / total_req) * 100)

        # 2. ROLE ALIGNMENT (25%)
        role_score = 60
        target_l = target_role.lower()
        title_l = job_title.lower()

        if target_l in title_l or title_l in target_l:
            role_score = 100
        elif any(w in title_l for w in target_l.split()):
            role_score = 85
        elif any(w in title_l for w in ["software", "developer", "engineer"]):
            role_score = 75

        # 3. EXPERIENCE MATCH (15%)
        exp_score = 85
        exp_status = "Good Match"
        exp_details = f"Candidate level '{experience_level}' fits job requirement '{job_exp_req}'."

        if "0-1" in job_exp_req or "0-2" in job_exp_req or "fresher" in job_exp_req.lower():
            exp_score = 100
            exp_status = "Direct Match"
            exp_details = f"Requirement '{job_exp_req}' is well matched for early-career / fresher candidates."
        elif "3+" in job_exp_req or "5+" in job_exp_req or "senior" in title_l:
            if experience_level in ["Advanced", "Senior"]:
                exp_score = 100
                exp_status = "Direct Match"
            else:
                exp_score = 60
                exp_status = "Experience Gap"
                exp_details = f"Job requests '{job_exp_req}' experience. Candidate profile is '{experience_level}'."

        # 4. EDUCATION MATCH (15%)
        edu_score = 80
        edu_status = "Matched"
        edu_details = "Candidate educational background aligns with engineering requirements."
        
        cand_degrees = []
        if user_education:
            for edu in user_education:
                deg = edu.get("degree", "").lower()
                cand_degrees.append(deg)

        deg_str = " ".join(cand_degrees)
        if any(d in deg_str for d in ["computer science", "b.tech", "btech", "m.tech", "mtech", "b.s", "bs", "m.s", "ms", "engineering"]):
            edu_score = 100
            edu_details = "Degree in Computer Science / Engineering matches requirement."
        elif user_education:
            edu_score = 85
            edu_details = f"Extracted education: {user_education[0].get('degree', 'Technical Degree')}."
        else:
            edu_score = 75
            edu_details = "Degree not explicitly specified in resume, evaluated based on skill proficiency."

        # 5. PROJECTS & TECHNICAL DEPTH (10%)
        proj_score = 70
        if user_projects and len(user_projects) >= 2:
            proj_score = 100
        elif user_projects and len(user_projects) == 1:
            proj_score = 85

        # OVERALL MATCH SCORE (0 - 100)
        overall_match = round(
            (0.35 * skills_score) +
            (0.25 * role_score) +
            (0.15 * exp_score) +
            (0.15 * edu_score) +
            (0.10 * proj_score)
        )
        overall_match = max(45, min(99, overall_match))

        # REASONS FOR RECOMMENDATION
        reasons = []
        if matching_skills:
            reasons.append(f"Strong overlap in key required skills: {', '.join(matching_skills[:4])}.")
        if role_score >= 85:
            reasons.append(f"High role alignment between target position '{target_role}' and '{job_title}'.")
        if edu_score >= 90:
            reasons.append("Educational qualifications directly match engineering criteria.")
        if user_projects:
            reasons.append(f"Extracted {len(user_projects)} practical projects demonstrating hands-on technical skills.")
        if not reasons:
            reasons.append("Fits candidate background and engineering skill profile.")

        # AREAS WHERE CANDIDATE IS WEAK
        weaknesses = []
        if missing_skills:
            weaknesses.append(f"Missing required technical competencies: {', '.join(missing_skills[:4])}.")
        if exp_score < 80:
            weaknesses.append(f"Experience gap: Role asks for '{job_exp_req}', while candidate profile is '{experience_level}'.")
        if skills_score < 60:
            weaknesses.append("Skill density for this specific job stack is below 60%. Recommend upskilling.")
        if not weaknesses:
            weaknesses.append("No critical skill or experience gaps identified for this role.")

        return {
            "id": str(job.get("id", job.get("_id", "job_1"))),
            "_id": str(job.get("_id", job.get("id", "job_1"))),
            "job_title": job_title,
            "company": job.get("company", "Tech Enterprise"),
            "location": job_location,
            "salary": job_salary,
            "experience_required": job_exp_req,
            "work_type": work_type,
            "match_score": overall_match,
            "breakdown": {
                "skills_score": skills_score,
                "role_score": role_score,
                "experience_score": exp_score,
                "education_score": edu_score,
                "projects_score": proj_score
            },
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "experience_match": {
                "score": exp_score,
                "user_level": experience_level,
                "required": job_exp_req,
                "status": exp_status,
                "details": exp_details
            },
            "education_match": {
                "score": edu_score,
                "required": "B.Tech / B.S. in CS or equivalent",
                "status": edu_status,
                "details": edu_details
            },
            "reasons_for_recommendation": reasons,
            "weaknesses": weaknesses,
            "job_url": job.get("url", job.get("job_url", "https://careers.google.com")),
            "source": job.get("source", "Verified Careers Portal"),
            "description": job.get("snippet", job.get("description", "")),
            "saved": bool(job.get("saved", False))
        }

    @classmethod
    def filter_and_sort_jobs(
        cls,
        matched_jobs: List[Dict[str, Any]],
        role_filter: Optional[str] = None,
        location_filter: Optional[str] = None,
        remote_filter: Optional[str] = None,
        experience_filter: Optional[str] = None,
        min_salary_filter: Optional[float] = None,
        required_skill_filter: Optional[str] = None,
        sort_by: str = "match_score"
    ) -> List[Dict[str, Any]]:
        filtered = list(matched_jobs)

        if role_filter and role_filter.strip() and role_filter != "All":
            rf = role_filter.lower().strip()
            filtered = [j for j in filtered if rf in j["job_title"].lower() or rf in j.get("company", "").lower()]

        if location_filter and location_filter.strip() and location_filter != "All":
            lf = location_filter.lower().strip()
            filtered = [j for j in filtered if lf in j["location"].lower()]

        if remote_filter and remote_filter.strip() and remote_filter != "All":
            rf = remote_filter.lower().strip()
            filtered = [j for j in filtered if j["work_type"].lower() == rf or rf in j["location"].lower()]

        if experience_filter and experience_filter.strip() and experience_filter != "All":
            ef = experience_filter.lower().strip()
            filtered = [j for j in filtered if ef in j["experience_required"].lower()]

        if min_salary_filter and min_salary_filter > 0:
            filtered = [j for j in filtered if cls.parse_salary_num(j["salary"]) >= min_salary_filter]

        if required_skill_filter and required_skill_filter.strip() and required_skill_filter != "All":
            sf = required_skill_filter.lower().strip()
            filtered = [
                j for j in filtered
                if any(sf in s.lower() for s in j["matching_skills"] + j["missing_skills"])
            ]

        # Sorting
        if sort_by == "relevance":
            filtered.sort(key=lambda j: (j["breakdown"]["role_score"], j["match_score"]), reverse=True)
        else:
            filtered.sort(key=lambda j: j["match_score"], reverse=True)

        return filtered
