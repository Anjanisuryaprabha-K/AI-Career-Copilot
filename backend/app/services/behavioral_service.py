class BehavioralService:
    @staticmethod
    def evaluate_star(situation: str, task: str, action: str, result: str, prompt: str = "") -> dict:
        sit_len = len(situation.split())
        task_len = len(task.split())
        act_len = len(action.split())
        res_len = len(result.split())
        
        has_metrics = "%" in result or any(char.isdigit() for char in result)
        has_first_person = "i " in action.lower() or "my " in action.lower() or "led" in action.lower() or "built" in action.lower()
        
        star_score = 0
        if sit_len >= 15: star_score += 20
        if task_len >= 10: star_score += 20
        if act_len >= 25 and has_first_person: star_score += 35
        if res_len >= 15 and has_metrics: star_score += 25
        
        star_score = max(50, min(100, star_score))
        grade = "Strong Hire (Exemplary STAR)" if star_score >= 85 else "Hire (Good Structure)" if star_score >= 70 else "Needs More Detail"
        
        return {
            "star_compliance_score": star_score,
            "hiring_verdict": grade,
            "breakdown": {
                "situation_clarity": "Strong context" if sit_len >= 15 else "Add more background",
                "task_definition": "Clear problem statement" if task_len >= 10 else "Define the specific challenge",
                "action_depth": "High personal ownership demonstrated" if has_first_person else "Highlight your specific individual contribution",
                "quantifiable_result": "Quantifiable metrics detected" if has_metrics else "Include numbers (e.g., % improvement, users impacted)"
            },
            "suggested_enhancement": f"To elevate your response, emphasize the measurable business impact: '{result.strip()} - which reduced operational latency and increased user retention by 25%'."
        }
