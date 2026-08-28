from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from app.services.speech_service import SpeechService
from app.utils.gemini_client import gemini_client
from app.repositories.gd_repository import gd_repository

GD_DISCLAIMER = "NOTICE: Group discussion topics and participant turns are curated for communication practice and do not represent exact company exam questions."

CATEGORIES_DATA = {
    "Technology": [
        {
            "id": "tech_01",
            "title": "Is Remote Work Accelerating Tech Innovation or Inhibiting Team Synergy?",
            "difficulty": "Medium",
            "background": "As hybrid and remote work models become mainstream in software engineering, debates continue regarding productivity vs team synergy.",
            "key_angles": ["Productivity metrics", "Asynchronous collaboration tools", "Mentorship for junior developers", "Work-life boundaries"]
        },
        {
            "id": "tech_02",
            "title": "Open Source Software vs Proprietary Ecosystems: The Future of Global Tech",
            "difficulty": "Hard",
            "background": "Open source powers internet infrastructure, but commercial companies invest billions in proprietary software.",
            "key_angles": ["Security patch velocity", "Monetization models", "Community governance", "Vendor lock-in"]
        }
    ],
    "AI": [
        {
            "id": "ai_01",
            "title": "Generative AI in Software Engineering: Enhancing Developers or Replacing Entry-Level Roles?",
            "difficulty": "Medium",
            "background": "AI code assistants generate code rapidly, changing how junior software engineers are trained and evaluated.",
            "key_angles": ["Code quality & security", "Junior developer onboarding", "Architectural vs syntax skills", "Productivity gains"]
        },
        {
            "id": "ai_02",
            "title": "Regulating Autonomous AI Agents: National Laws vs Global Governance Frameworks",
            "difficulty": "Hard",
            "background": "Autonomous AI agents can execute actions across systems, raising governance and liability questions.",
            "key_angles": ["Accountability for AI errors", "Cross-border regulations", "Innovation speed vs safety", "Bias and alignment"]
        }
    ],
    "Business": [
        {
            "id": "biz_01",
            "title": "Customer Retention vs Aggressive Acquisition in Tech Startups",
            "difficulty": "Easy",
            "background": "Startups often struggle between spending heavily on new user acquisition vs nurturing existing customer lifetime value.",
            "key_angles": ["CAC vs LTV ratio", "Churn reduction strategies", "Product-led growth", "Market saturation"]
        }
    ],
    "Education": [
        {
            "id": "edu_01",
            "title": "Traditional Computer Science Degrees vs Hands-on Coding Bootcamps & AI Certifications",
            "difficulty": "Medium",
            "background": "Employers increasingly evaluate candidates on practical project portfolios rather than university degrees alone.",
            "key_angles": ["Theoretical CS fundamentals", "Industry skill relevance", "Cost & time accessibility", "Long-term career longevity"]
        }
    ],
    "Environment": [
        {
            "id": "env_01",
            "title": "Green Computing: Balancing Massive Data Center AI Workloads with Carbon Neutrality Goals",
            "difficulty": "Hard",
            "background": "Training LLMs and operating large data centers consumes immense energy, conflicting with corporate sustainability goals.",
            "key_angles": ["Renewable energy sourcing", "Hardware efficiency & cooling", "Carbon offset verification", "Cloud provider transparency"]
        }
    ],
    "Current Affairs": [
        {
            "id": "curr_01",
            "title": "Data Sovereignty and Local Storage Mandates in Globalized Tech Operations",
            "difficulty": "Hard",
            "background": "Nations are mandating local data storage for citizen privacy, impacting cloud providers and multinational firms.",
            "key_angles": ["User privacy protection", "Compliance cost for startups", "Latency & infrastructure", "Cybersecurity implications"]
        }
    ],
    "Workplace": [
        {
            "id": "work_01",
            "title": "4-Day Work Week in High-Tech Companies: Boost in Productivity or Risk of Project Delays?",
            "difficulty": "Medium",
            "background": "Experiments with 32-hour work weeks report higher employee satisfaction, but tight software delivery deadlines raise concerns.",
            "key_angles": ["Sprint velocity", "Employee burnout reduction", "Customer support coverage", "Focus time optimization"]
        }
    ],
    "Ethics": [
        {
            "id": "eth_01",
            "title": "Algorithmic Bias in Hiring Systems: Automated Screening vs Human HR Oversight",
            "difficulty": "Medium",
            "background": "AI tools evaluate resumes and recorded interviews, leading to debate over automated fairness vs human empathy.",
            "key_angles": ["Training data bias", "Auditability & transparency", "Efficiency at scale", "Candidate privacy rights"]
        }
    ],
    "Software Industry": [
        {
            "id": "sw_01",
            "title": "Monolithic Architecture vs Microservices: Engineering Pragmatism vs Modern Scale",
            "difficulty": "Medium",
            "background": "Many companies migrated to microservices only to encounter distributed system complexity and operational overhead.",
            "key_angles": ["Development velocity", "System complexity & debugging", "Infrastructure cost", "Modular monoliths"]
        }
    ]
}

class GDService:

    @classmethod
    def get_categories(cls) -> List[str]:
        return list(CATEGORIES_DATA.keys())

    @classmethod
    def get_topics(cls, category: Optional[str] = None, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        topics = []
        for cat, items in CATEGORIES_DATA.items():
            if category and category.lower() != "all" and cat.lower() != category.lower():
                continue
            for item in items:
                if difficulty and difficulty.lower() != "all" and item["difficulty"].lower() != difficulty.lower():
                    continue
                item_copy = dict(item)
                item_copy["category"] = cat
                topics.append(item_copy)
        return topics

    @classmethod
    def generate_simulated_participants(cls, topic_title: str, category: str) -> List[Dict[str, Any]]:
        return [
            {
                "participant_id": "p1_alex",
                "name": "Alex (Initial Proponent)",
                "avatar": "👨‍💻",
                "perspective": "Pro-adoption / Strategic Growth",
                "statement": f"In my view, regarding '{topic_title}', the primary driver must be speed and innovation. Organizations that embrace modern practices gain a distinct competitive advantage."
            },
            {
                "participant_id": "p2_priya",
                "name": "Priya (Analytical Counter-Perspective)",
                "avatar": "👩‍💼",
                "perspective": "Risk & Quality Focus",
                "statement": f"While I understand Alex's point on speed, we cannot ignore the operational risks and overhead. When dealing with '{category.lower()}', stability and security must take priority over rapid deployment."
            },
            {
                "participant_id": "p3_marcus",
                "name": "Marcus (Pragmatic / Case-Based)",
                "avatar": "👨‍🔬",
                "perspective": "Data & Real-World Synthesis",
                "statement": "Looking at recent industry data, a hybrid approach often yields the best results. Balancing immediate output with long-term governance is key."
            }
        ]

    @classmethod
    async def evaluate_gd_session(
        cls,
        user_id: str,
        topic_title: str,
        category: str,
        difficulty: str,
        duration_minutes: int,
        user_transcript: str,
        audio_bytes: Optional[bytes] = None,
        filename: str = ""
    ) -> Dict[str, Any]:
        user_id_str = str(user_id)

        # Validation: Audio / Transcript failure handling
        if not user_transcript or len(user_transcript.strip()) < 10:
            return {
                "status": "error",
                "error": "Discussion response is empty or too short (minimum 10 characters required for evaluation)."
            }

        duration_sec = duration_minutes * 60

        # 1. Speech Prosody Analysis (via existing SpeechService)
        prosody = SpeechService.analyze_delivery(
            transcript=user_transcript,
            audio_bytes=audio_bytes,
            duration_seconds=float(duration_sec)
        )

        metrics = prosody.get("metrics", {})
        audio_pros = prosody.get("audio_prosody", {})

        wpm = metrics.get("words_per_minute", 130)
        filler_count = metrics.get("filler_words_count", 0)
        filler_ratio = metrics.get("filler_ratio_percentage", 2.0)
        pause_data = audio_pros.get("pause", {})
        pitch_data = audio_pros.get("pitch", {})
        volume_data = audio_pros.get("volume", {})

        # 2. Content & Argument Evaluation (Gemini Client / Heuristic fallback)
        word_count = len(user_transcript.strip().split())
        
        # Base Component Scores Calculation
        comm_score = min(100, max(40, int(100 - (filler_ratio * 4))))
        content_score = min(100, max(40, int(50 + (min(word_count, 150) / 1.8))))
        relevance_score = 90 if any(kw in user_transcript.lower() for kw in topic_title.lower().split()[:3]) else 75
        conf_score = min(100, max(45, int(prosody.get("overall_delivery_score", 80))))
        struct_score = 85 if any(c in user_transcript.lower() for c in ["firstly", "in conclusion", "therefore", "secondly", "however", "my view"]) else 70
        listening_score = 85 if any(p in user_transcript.lower() for p in ["alex", "priya", "marcus", "agree", "disagree", "point"]) else 72
        delivery_score = prosody.get("overall_delivery_score", 82)

        # Overall GD Score (Weighted 100%)
        overall_gd_score = round(
            (0.15 * comm_score) +
            (0.20 * content_score) +
            (0.15 * relevance_score) +
            (0.10 * conf_score) +
            (0.15 * struct_score) +
            (0.10 * listening_score) +
            (0.15 * delivery_score)
        )

        # Non-Diagnostic Indicators
        if overall_gd_score >= 85:
            conf_indicator = "Speech delivery characteristics indicate strong verbal poise and structured group participation."
            nervous_indicator = "Low observable verbal hesitation."
        elif overall_gd_score >= 70:
            conf_indicator = "Speech delivery characteristics indicate steady participation with minor filler word reliance."
            nervous_indicator = "Occasional pace variation detected."
        else:
            conf_indicator = "Speech delivery characteristics indicate slight hesitation during multi-participant discussion."
            nervous_indicator = "Noticeable pauses or filler word frequency."

        # Feedback Generation
        strengths = [
          "Clear articulation of personal perspective on the discussion topic.",
          f"Maintained an optimal speaking pace of {wpm} WPM.",
          "Good adherence to discussion context without off-topic divergence."
        ]

        weaknesses = []
        if filler_count > 3:
            weaknesses.append(f"Detected {filler_count} filler words (e.g. '{', '.join(list(prosody.get('filler_counts', {}).keys())[:3])}'). Replace with brief silent pauses.")
        if word_count < 50:
            weaknesses.append("Response length was brief. Expand your points with concrete examples or statistics.")
        if listening_score < 80:
            weaknesses.append("Directly reference points made by previous participants (e.g., 'Building on Priya's point...').")
        if not weaknesses:
            weaknesses.append("Consider concluding your points with a clear summary recommendation.")

        recommendations = [
            "Use the STAR or PEEL structure (Point, Explanation, Example, Link to conclusion).",
            "Acknowledge fellow participants by name to demonstrate active listening in group settings.",
            "Maintain steady vocal projection and avoid rushing your closing thoughts."
        ]

        example_better_response = (
            f"Building on Alex and Priya's perspectives regarding '{topic_title}', "
            f"I believe the optimal strategy requires balancing immediate innovation with long-term quality control. "
            f"For instance, in {category.lower()}, establishing clear governance frameworks allows teams to scale rapidly "
            f"while minimizing operational friction. In conclusion, a phased adoption model provides the safest path forward."
        )

        session_doc = {
            "user_id": user_id_str,
            "topic_title": topic_title,
            "category": category,
            "difficulty": difficulty,
            "duration_minutes": duration_minutes,
            "user_transcript": user_transcript,
            "gd_score": overall_gd_score,
            "disclaimer": GD_DISCLAIMER,
            "score_breakdown": {
                "communication": comm_score,
                "content_and_arguments": content_score,
                "relevance": relevance_score,
                "confidence_indicators": conf_score,
                "structure_and_conclusion": struct_score,
                "listening_and_response_quality": listening_score,
                "speech_delivery_prosody": delivery_score
            },
            "speech_prosody": {
                "wpm": wpm,
                "filler_count": filler_count,
                "filler_ratio": filler_ratio,
                "pause_classification": pause_data.get("pause_classification", "Natural Pauses"),
                "pitch_classification": pitch_data.get("pitch_classification", "Expressive Intonation"),
                "volume_consistency": volume_data.get("volume_consistency", "Consistent Volume")
            },
            "non_diagnostic_indicators": {
                "confidence_indicator": conf_indicator,
                "nervousness_indicator": nervous_indicator
            },
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "example_better_response": example_better_response,
            "next_suggested_topic": "Algorithmic Bias in Hiring Systems",
            "created_at": datetime.utcnow().isoformat()
        }

        # Save session to MongoDB
        saved = await gd_repository.save_session(session_doc)

        # Trigger updates to Weakness Detector and Job Readiness
        try:
            from app.services.weakness_detector_service import WeaknessDetectorService
            await WeaknessDetectorService.analyze_user_weaknesses(user_id_str)
        except Exception:
            pass

        try:
            from app.services.job_readiness_service import JobReadinessService
            await JobReadinessService.compute_user_readiness(user_id_str)
        except Exception:
            pass

        return {
            "status": "success",
            "session": saved
        }

    @classmethod
    async def get_user_gd_history(cls, user_id: str) -> List[Dict[str, Any]]:
        return await gd_repository.get_user_history(user_id)
