import re
from typing import Dict, Any, List, Optional
from app.utils.resume_parser import ResumeParser

EXTENDED_ROLE_SKILL_DATABASE = {
    "Full Stack Developer": [
        "React", "Node.js", "Express", "MongoDB", "JavaScript", "TypeScript",
        "HTML5", "CSS3", "Tailwind", "REST APIs", "Git", "Docker", "Redux", "SQL", "FastAPI", "PostgreSQL"
    ],
    "Frontend Developer": [
        "React", "JavaScript", "TypeScript", "HTML5", "CSS3", "Tailwind",
        "Next.js", "Redux", "Responsive Design", "REST APIs", "Git", "UI/UX", "Webpack", "Vite"
    ],
    "Backend Developer": [
        "Python", "FastAPI", "Django", "Node.js", "Express", "MongoDB",
        "PostgreSQL", "SQL", "Redis", "Docker", "REST APIs", "Microservices", "Git", "Kafka", "CI/CD"
    ],
    "Python Backend Engineer": [
        "Python", "FastAPI", "Django", "PostgreSQL", "MongoDB", "Redis", "Docker", "REST APIs", "Microservices", "SQL", "Git", "Asyncio"
    ],
    "MERN Specialist": [
        "React", "Node.js", "Express", "MongoDB", "JavaScript", "TypeScript", "Redux", "Tailwind CSS", "REST APIs", "Git", "JWT"
    ],
    "AI/ML Engineer": [
        "Python", "PyTorch", "TensorFlow", "Scikit-Learn", "Machine Learning",
        "Deep Learning", "NLP", "Pandas", "NumPy", "FastAPI", "Docker", "LLM", "Transformers", "LangChain"
    ],
    "Data Engineer": [
        "Python", "SQL", "Apache Spark", "Kafka", "Airflow", "PostgreSQL",
        "Snowflake", "BigQuery", "AWS", "ETL", "Data Pipelines", "Docker", "Hadoop"
    ],
    "DevOps / Cloud Engineer": [
        "Docker", "Kubernetes", "AWS", "CI/CD", "Terraform", "Linux",
        "GitHub Actions", "Prometheus", "Grafana", "Bash", "Python", "Nginx", "Ansible"
    ],
    "Software Engineer": [
        "Data Structures", "Algorithms", "Python", "Java", "C++", "JavaScript",
        "OOP", "System Design", "SQL", "Git", "REST APIs", "Debugging", "Linux"
    ]
}

COMMON_TECH_ENTITIES = [
    "python", "javascript", "typescript", "java", "c++", "c#", "golang", "rust", "ruby", "php", "dart", "swift", "kotlin",
    "react", "react.js", "angular", "vue", "next.js", "svelte", "tailwind", "bootstrap", "redux", "html5", "css3",
    "fastapi", "django", "flask", "node.js", "express", "spring boot", "asp.net", "graphql", "rest api", "grpc",
    "mongodb", "postgresql", "mysql", "redis", "elasticsearch", "cassandra", "dynamodb", "sqlite", "sqlite3",
    "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ansible", "jenkins", "github actions", "ci/cd",
    "kafka", "rabbitmq", "microservices", "system design", "load balancing", "distributed systems",
    "pytorch", "tensorflow", "scikit-learn", "pandas", "numpy", "machine learning", "deep learning", "nlp", "llm", "langchain",
    "git", "github", "linux", "bash", "agile", "scrum", "unit testing", "pytest", "jest", "data structures", "algorithms"
]

WEAK_VERBS_MAP = {
    "helped": "Spearheaded",
    "worked on": "Architected",
    "handled": "Engineered",
    "responsible for": "Executed",
    "assisted": "Orchestrated",
    "made": "Developed",
    "did": "Implemented",
    "looked after": "Optimized",
    "supported": "Pioneered",
    "created": "Formulated / Deployed"
}

KNOWN_TYPOS_DICTIONARY = {
    "develope": "develop",
    "developer": "developer",
    "reac": "React",
    "fastpi": "FastAPI",
    "mongdb": "MongoDB",
    "expereince": "experience",
    "mangement": "management",
    "responsbile": "responsible",
    "implment": "implement",
    "enginere": "engineer",
    "softare": "software",
    "maintenence": "maintenance",
    "pogramming": "programming",
    "architectue": "architecture"
}

class LiveATSScorer:
    @staticmethod
    def discover_role_benchmarks(target_role: str, custom_jd: str = "", company_context: str = "") -> List[str]:
        role_key = None
        for k in EXTENDED_ROLE_SKILL_DATABASE:
            if k.lower() in target_role.lower() or target_role.lower() in k.lower():
                role_key = k
                break
        
        benchmarks = list(EXTENDED_ROLE_SKILL_DATABASE.get(role_key, EXTENDED_ROLE_SKILL_DATABASE["Software Engineer"]))

        combined_context = f"{target_role} {company_context} {custom_jd}".lower()
        extracted_dynamic_skills = []
        for tech in COMMON_TECH_ENTITIES:
            pattern = r"\b" + re.escape(tech) + r"\b"
            if re.search(pattern, combined_context):
                formatted_tech = tech.title()
                if formatted_tech.lower() in ["sql", "aws", "gcp", "llm", "nlp", "etl", "ci/cd", "ui/ux"]:
                    formatted_tech = formatted_tech.upper()
                if formatted_tech not in benchmarks:
                    extracted_dynamic_skills.append(formatted_tech)

        return list(dict.fromkeys(benchmarks + extracted_dynamic_skills))

    @classmethod
    def calculate_live_score(
        cls,
        resume_text: str,
        target_role: str = "Software Engineer",
        custom_jd: str = "",
        company_name: str = ""
    ) -> Dict[str, Any]:
        text_lower = resume_text.lower()
        words = re.findall(r"\b[a-zA-Z]+\b", text_lower)
        word_count = len(words)

        # Extract structured content
        structured = ResumeParser.parse_full_structured(resume_text)

        # 1. Section Completeness (20% = Max 20 pts)
        sections_detected = []
        completeness_raw = 0
        section_weights = {
            "experience": 5,
            "skills": 5,
            "education": 4,
            "projects": 4,
            "certifications": 2
        }
        for sec, pts in section_weights.items():
            if re.search(r"\b" + sec + r"\b", text_lower):
                sections_detected.append(sec.capitalize())
                completeness_raw += pts

        score_completeness = min(20, completeness_raw)

        # 2. Quantifiable Impact & Power Verbs (25% = Max 25 pts)
        metric_matches = re.findall(
            r"(\d+%\s*|\$\d+|\d+x|\d+\s*(users|clients|requests|ms|seconds|million|k|fps|gb|mb))",
            text_lower
        )
        weak_verbs_found = []
        for weak, strong in WEAK_VERBS_MAP.items():
            if re.search(r"\b" + re.escape(weak) + r"\b", text_lower):
                weak_verbs_found.append({"found": weak, "suggested": strong})

        metrics_pts = min(15, len(metric_matches) * 5)
        verbs_pts = max(0, 10 - (len(weak_verbs_found) * 3))
        score_impact = min(25, metrics_pts + verbs_pts)

        # 3. Skill Density & Technical Keywords (25% = Max 25 pts)
        target_skills = cls.discover_role_benchmarks(target_role, custom_jd, company_name)
        matched_keywords = []
        missing_keywords = []

        for skill in target_skills:
            pattern = r"\b" + re.escape(skill.lower()) + r"\b"
            if re.search(pattern, text_lower):
                matched_keywords.append(skill)
            else:
                missing_keywords.append(skill)

        keyword_match_pct = (len(matched_keywords) / max(1, len(target_skills))) * 100
        score_skills = min(25, round((keyword_match_pct / 100) * 25))

        # 4. Spelling & Grammar Health (15% = Max 15 pts)
        spelling_errors = []
        for w in words:
            if w in KNOWN_TYPOS_DICTIONARY:
                if not any(e["word"] == w for e in spelling_errors):
                    spelling_errors.append({
                        "word": w,
                        "suggested": KNOWN_TYPOS_DICTIONARY[w],
                        "context": f"Found typo '{w}' - suggested correction '{KNOWN_TYPOS_DICTIONARY[w]}'"
                    })

        score_spelling = max(0, round(15 - (len(spelling_errors) * 2.5)))

        # 5. ATS Formatting & Readability (15% = Max 15 pts)
        contact_info = structured["contact_info"]
        has_bullets = bool(re.search(r"[\bullet\*\-\u2022]\s+", resume_text))
        
        format_pts = 0
        if 250 <= word_count <= 1200: format_pts += 5
        if has_bullets: format_pts += 4
        if contact_info["has_email"]: format_pts += 3
        if contact_info["has_phone"]: format_pts += 3
        score_formatting = min(15, format_pts)

        # Total Mathematically Calculated Overall Score (0 to 100)
        overall_score = score_completeness + score_impact + score_skills + score_spelling + score_formatting
        overall_score = max(10, min(100, overall_score))

        # SECTION-LEVEL SCORES (0-100 for each section)
        sec_contact_score = 100 if (contact_info["has_email"] and contact_info["has_phone"]) else (65 if (contact_info["has_email"] or contact_info["has_phone"]) else 30)
        sec_skills_score = min(100, round((len(matched_keywords) / max(1, len(target_skills))) * 100))
        sec_exp_score = min(100, (30 if structured["experience"] else 0) + min(40, len(metric_matches) * 10) + (30 if not weak_verbs_found else 15))
        sec_proj_score = min(100, (50 if structured["projects"] else 0) + min(50, len(structured["projects"]) * 25))
        sec_edu_score = 90 if structured["education"] else 40
        sec_cert_score = 90 if structured["certifications"] else 50
        sec_achieve_score = 90 if structured["achievements"] else 45

        section_scores = {
            "contact_info": {
                "score": sec_contact_score,
                "status": "Strong" if sec_contact_score > 80 else ("Moderate" if sec_contact_score >= 60 else "Weak"),
                "recommendation": "Add full email, phone, LinkedIn, and GitHub links." if sec_contact_score < 80 else "Contact details are well formatted."
            },
            "skills": {
                "score": sec_skills_score,
                "status": "Strong" if sec_skills_score > 80 else ("Moderate" if sec_skills_score >= 60 else "Weak"),
                "recommendation": f"Add missing industry skills: {', '.join(missing_keywords[:4])}." if missing_keywords else "High skill density."
            },
            "experience": {
                "score": sec_exp_score,
                "status": "Strong" if sec_exp_score > 80 else ("Moderate" if sec_exp_score >= 60 else "Weak"),
                "recommendation": "Add quantifiable impact metrics (% performance gains, revenue) to experience bullets." if sec_exp_score < 80 else "Solid work experience bullets."
            },
            "projects": {
                "score": sec_proj_score,
                "status": "Strong" if sec_proj_score > 80 else ("Moderate" if sec_proj_score >= 60 else "Weak"),
                "recommendation": "Include at least 2 technical projects highlighting full-stack/system architecture." if sec_proj_score < 80 else "Projects are clearly described."
            },
            "education": {
                "score": sec_edu_score,
                "status": "Strong" if sec_edu_score > 80 else "Weak",
                "recommendation": "Mention degree, major, and graduation year clearly." if sec_edu_score < 80 else "Education background identified."
            },
            "certifications": {
                "score": sec_cert_score,
                "status": "Strong" if sec_cert_score > 80 else "Moderate",
                "recommendation": "Add industry certifications (AWS, Meta, Coursera) to strengthen resume." if sec_cert_score < 80 else "Certifications present."
            },
            "achievements": {
                "score": sec_achieve_score,
                "status": "Strong" if sec_achieve_score > 80 else "Moderate",
                "recommendation": "Include hackathons, competitive programming rankings, or awards." if sec_achieve_score < 80 else "Key achievements listed."
            }
        }

        # WEAK RESUME SECTIONS
        weak_sections = []
        for sec_name, data in section_scores.items():
            if data["score"] < 65:
                weak_sections.append({
                    "section": sec_name.replace("_", " ").title(),
                    "score": data["score"],
                    "issue": f"{sec_name.replace('_', ' ').title()} section scored low ({data['score']}/100).",
                    "recommendation": data["recommendation"]
                })

        # CANDIDATE STRENGTHS
        strengths = []
        if sec_skills_score >= 70:
            strengths.append(f"Strong alignment with target role '{target_role}' with {len(matched_keywords)} matched technical skills.")
        if len(metric_matches) >= 2:
            strengths.append(f"High quantifiable impact: Detected {len(metric_matches)} data-driven metrics in experience/projects.")
        if contact_info["has_email"] and contact_info["has_phone"]:
            strengths.append("Complete, ATS-compliant contact header including email and phone.")
        if len(spelling_errors) == 0:
            strengths.append("Flawless spelling and grammar with zero typos detected.")
        if structured["projects"]:
            strengths.append(f"Demonstrates practical hands-on experience through {len(structured['projects'])} featured projects.")
        if not strengths:
            strengths.append("Clear structural section layout with readable formatting.")

        # JOB DESCRIPTION COMPARISON
        jd_matched_kw = []
        jd_missing_kw = []
        jd_match_percentage = 0
        jd_strengths = []
        jd_gap_recommendations = []

        if custom_jd.strip():
            jd_words = re.findall(r"\b[a-zA-Z0-9+#.-]+\b", custom_jd.lower())
            jd_techs = []
            for tech in COMMON_TECH_ENTITIES:
                if tech in custom_jd.lower():
                    formatted = tech.title() if tech not in ["sql", "aws", "gcp", "ci/cd"] else tech.upper()
                    jd_techs.append(formatted)
            jd_techs = list(set(jd_techs))

            for kw in jd_techs:
                if kw in matched_keywords or re.search(r"\b" + re.escape(kw.lower()) + r"\b", text_lower):
                    jd_matched_kw.append(kw)
                else:
                    jd_missing_kw.append(kw)

            jd_match_percentage = min(100, round((len(jd_matched_kw) / max(1, len(jd_techs))) * 100)) if jd_techs else overall_score
            
            if jd_matched_kw:
                jd_strengths.append(f"Matches {len(jd_matched_kw)} required technical competencies from the job description.")
            if jd_missing_kw:
                for kw in jd_missing_kw[:3]:
                    jd_gap_recommendations.append(f"Job Description explicitly requires '{kw}' which is missing from your resume text.")
        else:
            jd_match_percentage = overall_score
            jd_matched_kw = matched_keywords
            jd_missing_kw = missing_keywords

        # Actionable Checklist Items & Badges
        action_checklist = []
        critical_fixes = []
        content_improvements = []
        missing_skills_recommendations = []

        if not contact_info["has_email"]:
            critical_fixes.append("Missing contact email. ATS parsers require an email to index candidate profiles.")
            action_checklist.append({"id": "act_email", "task": "Add email address to header", "badge": "Critical Fix", "badge_color": "rose", "resolved": False})

        if spelling_errors:
            for err in spelling_errors:
                critical_fixes.append(f"Spelling typo '{err['word']}': Replace with '{err['suggested']}'.")
                action_checklist.append({"id": f"act_spell_{err['word']}", "task": f"Fix typo '{err['word']}' -> '{err['suggested']}'", "badge": "Critical Fix", "badge_color": "rose", "resolved": False})

        if missing_keywords:
            for kw in missing_keywords[:4]:
                missing_skills_recommendations.append(f"Add key technical skill: '{kw}'")
                action_checklist.append({"id": f"act_kw_{kw}", "task": f"Add missing skill '{kw}' into Skills or Experience section", "badge": "Missing Skill", "badge_color": "amber", "resolved": False})

        if len(metric_matches) < 3:
            content_improvements.append("Lacking quantifiable metrics. Add numbers, percentages (%), or dollar ($) results.")
            action_checklist.append({"id": "act_metrics", "task": "Add at least 3 quantifiable metrics to work experience bullet points", "badge": "Content Upgrade", "badge_color": "amber", "resolved": False})

        if weak_verbs_found:
            for wv in weak_verbs_found[:3]:
                content_improvements.append(f"Replace passive verb '{wv['found']}' with action power verb '{wv['suggested']}'.")
                action_checklist.append({"id": f"act_verb_{wv['found']}", "task": f"Replace passive phrase '{wv['found']}' with '{wv['suggested']}'", "badge": "Content Upgrade", "badge_color": "amber", "resolved": False})

        if contact_info["has_email"] and contact_info["has_phone"]:
            action_checklist.append({"id": "pass_contact", "task": "Contact details present and verified", "badge": "Passed Check", "badge_color": "emerald", "resolved": True})

        if has_bullets:
            action_checklist.append({"id": "pass_bullets", "task": "ATS bullet point formatting verified", "badge": "Passed Check", "badge_color": "emerald", "resolved": True})

        # DYNAMIC LEARNING ROADMAP GENERATION POST ATS SCORE
        roadmap_phases = []
        
        # Phase 1: Bridge Technical Skill Gaps
        p1_items = []
        for kw in missing_keywords[:4]:
            p1_items.append({
                "id": f"p1_{kw.lower().replace(' ', '_').replace('.', '_')}",
                "task": f"Master {kw} core principles & practical usage",
                "category": "Technical Skill Gap",
                "resource": "Official Docs & Guided Tutorials",
                "completed": False
            })
        if not p1_items:
            p1_items.append({
                "id": "p1_advanced",
                "task": f"Deepen advanced concepts in {target_role} architecture",
                "category": "Advanced Specialization",
                "resource": "Industry Case Studies",
                "completed": False
            })
        
        roadmap_phases.append({
            "phase": 1,
            "title": "Phase 1: Bridge Missing Technical Competencies",
            "duration": "1 - 2 Weeks",
            "focus": f"Master key technical skills missing for {target_role}",
            "items": p1_items
        })
        
        # Phase 2: Resume & Portfolio Impact Upgrade
        p2_items = []
        if weak_sections:
            for ws in weak_sections[:2]:
                p2_items.append({
                    "id": f"p2_{ws['section'].lower().replace(' ', '_')}",
                    "task": f"Upgrade {ws['section']}: {ws['recommendation']}",
                    "category": "Resume Enhancement",
                    "resource": "ATS Optimization Assistant",
                    "completed": False
                })
        p2_items.append({
            "id": "p2_metrics",
            "task": "Add at least 3 quantifiable performance metrics (% speedup, scale, $ saved)",
            "category": "Bullet Point Quality",
            "resource": "Impact Metric Builder",
            "completed": False
        })
        
        roadmap_phases.append({
            "phase": 2,
            "title": "Phase 2: High-Impact Portfolio & Resume Optimization",
            "duration": "1 - 2 Weeks",
            "focus": "Quantified accomplishment metrics & structural polish",
            "items": p2_items
        })
        
        # Phase 3: Coding Arena & Technical Interview Execution
        roadmap_phases.append({
            "phase": 3,
            "title": "Phase 3: Coding Arena & Mock Interview Mastery",
            "duration": "2 Weeks",
            "focus": "Technical problem solving & voice prosody interview practice",
            "items": [
                {
                    "id": "p3_coding",
                    "task": f"Complete 5+ {target_role} problems in Coding Arena",
                    "category": "Technical Problem Solving",
                    "resource": "Coding Arena IDE",
                    "completed": False
                },
                {
                    "id": "p3_interview",
                    "task": "Complete a 3-question AI Voice Prosody Mock Interview session",
                    "category": "Speech & Prosody",
                    "resource": "AI Voice Prosody Analyzer",
                    "completed": False
                }
            ]
        })
        
        learning_roadmap = {
            "target_role": target_role,
            "overall_ats_score": overall_score,
            "estimated_timeframe": "4 - 6 Weeks",
            "total_action_items": sum(len(p["items"]) for p in roadmap_phases),
            "phases": roadmap_phases
        }

        return {
            "overall_score": overall_score,
            "target_role": target_role,
            "breakdown": {
                "section_completeness": score_completeness,   # Max 20 pts
                "quantifiable_impact": score_impact,           # Max 25 pts
                "skill_density": score_skills,                 # Max 25 pts
                "spelling_grammar": score_spelling,            # Max 15 pts
                "ats_formatting": score_formatting             # Max 15 pts
            },
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "weak_verbs_detected": weak_verbs_found,
            "spelling_errors": spelling_errors,
            "sections_detected": sections_detected,
            "contact_info_detected": contact_info,
            "word_count": word_count,
            "critical_fixes": critical_fixes,
            "content_improvements": content_improvements,
            "missing_skills_recommendations": missing_skills_recommendations,
            "action_item_checklist": action_checklist,
            "learning_roadmap": learning_roadmap,
            "structured_extraction": structured,
            "section_scores": section_scores,
            "weak_sections": weak_sections,
            "strengths": strengths,
            "jd_match_analysis": {
                "jd_provided": bool(custom_jd.strip()),
                "match_percentage": jd_match_percentage,
                "matched_keywords": jd_matched_kw,
                "missing_keywords": jd_missing_kw,
                "strengths": jd_strengths,
                "gap_recommendations": jd_gap_recommendations
            }
        }
