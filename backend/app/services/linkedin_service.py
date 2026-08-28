class LinkedInService:
    @staticmethod
    def optimize_profile(target_role: str, current_skills: list, experience_level: str = "Entry Level / Student"):
        top_skills = ", ".join(current_skills[:5]) if current_skills else "Full Stack | Python | React | DSA"
        return {
            "target_role": target_role,
            "profile_strength_score": 84,
            "headline_suggestions": [
                f"{target_role} | Ex-Intern | {top_skills} | Building High-Scale Web Apps",
                f"Aspiring {target_role} | 300+ LeetCode | Passionate about Distributed Systems & Cloud",
                f"Full-Stack Software Engineer | MERN & FastAPI Specialist | Open Source Contributor"
            ],
            "about_summary": f"I am a results-driven {target_role} with deep passion for building high-performance systems and intuitive user experiences. Proficient in {top_skills}, I thrive in collaborative environments where solving complex data structures and backend scalability challenges is key.\n\nAlways open to discussing software engineering roles, hackathons, and innovative open-source projects.",
            "top_keywords_to_add": ["Microservices", "RESTful APIs", "CI/CD Pipeline", "Agile/Scrum", "Cloud Infrastructure", "System Design"],
            "action_plan": [
                "Feature your top 2 GitHub projects with live demo links in the 'Featured' section.",
                "Request 2 recommendations from internship mentors or team project leads.",
                "Join and participate in active engineering groups related to " + target_role + "."
            ]
        }
