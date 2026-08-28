class PortfolioService:
    @staticmethod
    def get_portfolio_template(user_name: str, target_role: str, bio: str, skills: list, projects: list):
        return {
            "user_name": user_name,
            "target_role": target_role,
            "bio": bio or "Passionate software engineer building resilient digital experiences.",
            "skills": skills or ["Python", "JavaScript", "React", "FastAPI", "MongoDB", "Docker"],
            "projects": projects or [
                {
                    "title": "AI Career Readiness & Placement Platform",
                    "description": "Full-stack AI platform with live ATS scoring, mock interviews, and coding arena.",
                    "technologies": ["FastAPI", "React", "MongoDB", "WebSockets"],
                    "live_url": "https://career-mentor-demo.app",
                    "github_url": "https://github.com/preetham/career-platform"
                },
                {
                    "title": "Learning-to-Rank Search Engine",
                    "description": "Implemented LambdaMART and LightGBM ranking algorithms over MSLR-10K dataset.",
                    "technologies": ["Python", "LightGBM", "Scikit-Learn", "FastAPI"],
                    "live_url": "",
                    "github_url": "https://github.com/preetham/ltr-ranking"
                }
            ],
            "social_links": {
                "github": f"https://github.com/{user_name.lower().replace(' ', '')}",
                "linkedin": f"https://linkedin.com/in/{user_name.lower().replace(' ', '-')}",
                "email": f"{user_name.lower().replace(' ', '')}@example.com"
            },
            "theme": "modern-dark"
        }
