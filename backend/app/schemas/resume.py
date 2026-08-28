from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TextAnalysisRequest(BaseModel):
    resume_text: str
    target_role: Optional[str] = "Software Engineer"
    custom_jd: Optional[str] = ""
    company_name: Optional[str] = ""

class BulletRewriteRequest(BaseModel):
    bullet_point: str
    action_verb: Optional[str] = "Engineered"

class BenchmarkSearchRequest(BaseModel):
    target_role: str
    company_name: Optional[str] = ""
    custom_jd: Optional[str] = ""

class SpellingErrorItem(BaseModel):
    word: str
    suggested: str
    context: Optional[str] = ""

class ScoreBreakdown(BaseModel):
    section_completeness: int  # Max 20 pts
    quantifiable_impact: int   # Max 25 pts
    skill_density: int          # Max 25 pts
    spelling_grammar: int       # Max 15 pts
    ats_formatting: int         # Max 15 pts

class ResumeScanReportResponse(BaseModel):
    overall_score: int
    target_role: str
    breakdown: ScoreBreakdown
    matched_keywords: List[str]
    missing_keywords: List[str]
    weak_verbs_detected: List[Dict[str, str]]
    spelling_errors: List[SpellingErrorItem]
    sections_detected: List[str]
    contact_info_detected: Dict[str, Any]
    critical_fixes: List[str]
    content_improvements: List[str]
    missing_skills_recommendations: List[str]
    action_item_checklist: List[Dict[str, Any]]
    structured_extraction: Optional[Dict[str, Any]] = None
    section_scores: Optional[Dict[str, Any]] = None
    weak_sections: Optional[List[Dict[str, Any]]] = None
    strengths: Optional[List[str]] = None
    jd_match_analysis: Optional[Dict[str, Any]] = None
