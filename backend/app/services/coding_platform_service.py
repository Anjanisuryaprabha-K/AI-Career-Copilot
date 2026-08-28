import urllib.request
import json
from typing import Dict, Any

class CodingPlatformService:
    @classmethod
    def fetch_leetcode_profile(cls, username: str) -> Dict[str, Any]:
        clean_name = (username or "").strip()
        if not clean_name:
            return {
                "status": "unlinked",
                "username": "",
                "isConnected": False,
                "is_available": False,
                "message": "No LeetCode handle connected."
            }

        # Attempt real network fetch from public LeetCode stats API / GraphQL
        url = f"https://leetcode-stats-api.herokuapp.com/{clean_name}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    if data.get("status") == "success":
                        return {
                            "status": "success",
                            "is_available": True,
                            "username": clean_name,
                            "isConnected": True,
                            "totalSolved": data.get("totalSolved", 0),
                            "easySolved": data.get("easySolved", 0),
                            "mediumSolved": data.get("mediumSolved", 0),
                            "hardSolved": data.get("hardSolved", 0),
                            "streak": data.get("ranking", 0),
                            "acceptanceRate": data.get("acceptanceRate", 0),
                            "totalQuestions": data.get("totalQuestions", 0),
                            "badges": ["LeetCode Verified"]
                        }
        except Exception:
            pass

        # If external service is unavailable or rate limited, return explicit unavailable state
        return {
            "status": "unavailable",
            "is_available": False,
            "username": clean_name,
            "isConnected": True,
            "message": "External LeetCode profile service is currently unreachable. Handle preserved.",
            "totalSolved": None,
            "easySolved": None,
            "mediumSolved": None,
            "hardSolved": None,
            "streak": None,
            "badges": []
        }

    @classmethod
    def fetch_hackerrank_profile(cls, username: str) -> Dict[str, Any]:
        clean_name = (username or "").strip()
        if not clean_name:
            return {
                "status": "unlinked",
                "username": "",
                "isConnected": False,
                "is_available": False,
                "message": "No HackerRank handle connected."
            }

        url = f"https://www.hackerrank.com/rest/hackers/{clean_name}/profile"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    model = data.get("model", {})
                    return {
                        "status": "success",
                        "is_available": True,
                        "username": clean_name,
                        "isConnected": True,
                        "name": model.get("name", clean_name),
                        "created_at": model.get("created_at", ""),
                        "level": model.get("level", 1),
                        "badges": model.get("badges", [])
                    }
        except Exception:
            pass

        return {
            "status": "unavailable",
            "is_available": False,
            "username": clean_name,
            "isConnected": True,
            "message": "External HackerRank profile service is currently unreachable. Handle preserved.",
            "badges": []
        }
