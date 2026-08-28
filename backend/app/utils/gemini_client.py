"""
Google Gemini & AI Provider Integration Client.
Provides text generation using Google Gemini / AI APIs with fallback support.
"""
import os
import httpx
from typing import Optional
from app.config import settings

class GeminiClient:
    def __init__(self):
        self.api_key = settings.GOOGLE_API_KEY or settings.AI_API_KEY or os.getenv("GOOGLE_API_KEY", "")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    async def generate_text(self, prompt: str) -> str:
        if not self.api_key:
            return ""

        try:
            url = f"{self.api_url}?key={self.api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }

            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "").strip()
        except Exception as e:
            print(f"[GeminiClient Error] {e}")

        return ""

gemini_client = GeminiClient()
