class ResumeExportService:
    @staticmethod
    def generate_latex_resume(user_name: str = "Preetham V", email: str = "preetham@placement.edu", skills: list = None):
        skills_str = ", ".join(skills or ["Python", "FastAPI", "React", "MongoDB", "Data Structures", "Docker"])
        
        latex_code = f"""\\documentclass[letterpaper,10pt]{{article}}
\\usepackage[left=0.5in,top=0.5in,right=0.5in,bottom=0.5in]{{geometry}}
\\usepackage{{hyperref}}

\\begin{{document}}
\\begin{{center}}
    {{\\Large \\textbf{{{user_name}}}}} \\\\
    \\href{{mailto:{email}}}{{{email}}} | \\href{{https://github.com/preetham}}{{github.com/preetham}}
\\end{{center}}

\\section*{{EDUCATION}}
\\textbf{{Bachelor of Technology in Computer Science and Engineering}} \\hfill 2023 -- 2027

\\section*{{TECHNICAL SKILLS}}
\\textbf{{Languages \\& Frameworks:}} {skills_str}

\\section*{{PROJECTS}}
\\textbf{{AI Career Readiness \\& Placement Mentor Platform}} \\hfill React, FastAPI, MongoDB \\\\
- Architected end-to-end placement readiness system with real-time ATS scoring and mock interviews.

\\section*{{ACHIEVEMENTS}}
- Solved 300+ Algorithmic Challenges across LeetCode and CodeChef.
\\end{{document}}"""

        return {
            "format": "LaTeX (Overleaf Compatible)",
            "latex_source": latex_code,
            "filename": f"{user_name.replace(' ', '_')}_ATS_Resume.tex"
        }
