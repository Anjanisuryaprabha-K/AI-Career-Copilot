class OAService:
    @staticmethod
    def get_oa_test_config(company: str = "Amazon"):
        return {
            "test_title": f"{company} Placement Online Assessment (OA)",
            "total_duration_mins": 75,
            "sections": [
                {
                    "section_id": "sec_aptitude",
                    "title": "Aptitude & Core CS Fundamentals",
                    "duration_mins": 25,
                    "questions_count": 15,
                    "topics": ["Operating Systems", "DBMS", "Computer Networks", "Quantitative Logic"]
                },
                {
                    "section_id": "sec_coding",
                    "title": "Algorithmic Coding Section",
                    "duration_mins": 50,
                    "questions_count": 2,
                    "problems": [
                        {
                            "id": "oa_q1",
                            "title": "Minimum Operations to Balance Server Loads",
                            "difficulty": "Medium",
                            "score": 50,
                            "starter_code": "def minServerOperations(servers: list[int]) -> int:\n    # Write your solution here\n    pass"
                        },
                        {
                            "id": "oa_q2",
                            "title": "Optimize Delivery Fleet Routes",
                            "difficulty": "Medium-Hard",
                            "score": 50,
                            "starter_code": "def optimizeFleet(capacity: int, deliveries: list[list[int]]) -> int:\n    # Write your solution here\n    pass"
                        }
                    ]
                }
            ]
        }

    @staticmethod
    def evaluate_oa_submission(answers: dict):
        aptitude_score = answers.get("aptitude_score", 13)
        coding_tests_passed = answers.get("coding_tests_passed", 6)
        total_tests = answers.get("total_coding_tests", 6)
        
        pct = round(((aptitude_score / 15) * 40) + ((coding_tests_passed / total_tests) * 60))
        status = "Qualified for Technical Rounds" if pct >= 70 else "Needs Practice"
        
        return {
            "overall_score_percentage": pct,
            "qualification_status": status,
            "percentile_rank": "Top 12% among batch applicants",
            "section_breakdown": {
                "aptitude_score": f"{aptitude_score}/15 ({(aptitude_score/15)*100:.0f}%)",
                "coding_score": f"{coding_tests_passed}/{total_tests} Test Cases ({(coding_tests_passed/total_tests)*100:.0f}%)"
            },
            "recommendations": [
                "Great work on algorithmic correctness!",
                "Review edge case constraints regarding large input arrays in under 2.0 seconds."
            ]
        }
