class ChatService:
    @staticmethod
    def get_ai_response(user_message: str, history: list = None) -> dict:
        msg_lower = user_message.lower()
        if "resume" in msg_lower or "ats" in msg_lower:
            reply = "To maximize your ATS score, use standard section titles (Experience, Skills, Projects, Education), include quantifiable metrics (e.g., 'improved query latency by 35%'), and ensure you mirror key terminology from the target job description."
        elif "interview" in msg_lower or "mock" in msg_lower:
            reply = "For behavioral and situational interview questions, structure your answers using the STAR method: Situation, Task, Action, and Result. For technical rounds, remember to verbalize your thought process and calculate Time & Space complexity before writing code."
        elif "coding" in msg_lower or "dsa" in msg_lower or "leetcode" in msg_lower:
            reply = "When tackling algorithmic problems, start by clarifying edge cases (empty inputs, negative values). Then describe your brute force approach, optimize it using suitable data structures (e.g., Two Pointers, Sliding Window, Monotonic Stack, or Hash Maps), and write clean, modular code."
        elif "roadmap" in msg_lower or "skills" in msg_lower:
            reply = "Based on current market requirements, prioritize mastering core CS fundamentals (DSA, Operating Systems, DBMS), building 2 production-grade full-stack projects with CI/CD and Docker, and maintaining daily coding consistency."
        else:
            reply = f"Hello! I am your AI Career Mentor. I can help you review your resume, prepare for technical & HR interviews, solve coding challenges, and track your placement readiness. What would you like to work on today?"
            
        return {
            "response": reply,
            "suggestions": [
                "How do I improve my ATS score above 80%?",
                "What are the top 5 questions asked in Full Stack interviews?",
                "Give me a study plan for Two Pointers and Sliding Window"
            ]
        }
