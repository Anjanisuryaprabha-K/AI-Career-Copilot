class AdminPortalService:
    @staticmethod
    def get_batch_analytics():
        return {
            "total_students_enrolled": 120,
            "placement_ready_students": 78,
            "average_batch_readiness_score": 76.4,
            "tier_distribution": {
                "Tier 1 (>85% Readiness)": 38,
                "Tier 2 (70-84% Readiness)": 52,
                "Tier 3 (<70% Readiness)": 30
            },
            "top_recruiter_drives": [
                {"company": "Amazon", "eligible_count": 54, "drive_date": "August 28, 2026"},
                {"company": "Swiggy", "eligible_count": 68, "drive_date": "September 2, 2026"},
                {"company": "Razorpay", "eligible_count": 62, "drive_date": "September 10, 2026"}
            ],
            "shortlisted_students": [
                {"id": "st_1", "name": "Preetham V", "cgpa": 8.8, "readiness": 88, "solved_dsa": 310, "status": "Tier 1 Verified"},
                {"id": "st_2", "name": "Aditya K", "cgpa": 8.5, "readiness": 84, "solved_dsa": 260, "status": "Tier 1 Verified"},
                {"id": "st_3", "name": "Sneha R", "cgpa": 9.1, "readiness": 89, "solved_dsa": 340, "status": "Tier 1 Verified"}
            ]
        }
