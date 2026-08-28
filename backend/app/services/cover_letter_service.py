from datetime import datetime

class CoverLetterService:
    @staticmethod
    def generate_cover_letter(user_name: str, target_role: str, company_name: str, skills: list, experience_summary: str = "") -> dict:
        skills_str = ", ".join(skills[:5]) if skills else "modern software engineering practices, algorithms, and full-stack development"
        
        body = f"""Dear Hiring Team at {company_name},

I am writing to express my strong interest in the {target_role} position at {company_name}. With hands-on experience in {skills_str}, I am confident in my ability to deliver high-quality, scalable solutions and contribute effectively to your team's mission.

Throughout my technical journey, {experience_summary if experience_summary else "I have built and deployed robust full-stack applications, focused on system performance, and solved challenging algorithmic problems."} My commitment to clean code architecture, problem-solving, and continuous learning aligns seamlessly with the dynamic work culture at {company_name}.

I am excited about the opportunity to bring my technical expertise and problem-solving skills to {company_name}. Thank you for your time and consideration. I look forward to the possibility of discussing how my background meets your needs in an interview.

Sincerely,
{user_name}"""

        return {
            "applicant_name": user_name,
            "target_role": target_role,
            "company_name": company_name,
            "generated_date": datetime.utcnow().strftime("%B %d, %Y"),
            "cover_letter_text": body,
            "word_count": len(body.split()),
            "strengths_highlighted": skills[:4] if skills else ["Full Stack", "Problem Solving", "System Architecture"]
        }
