import re
from urllib.parse import quote_plus, urlparse
from typing import Dict, Any, List, Optional
from app.services.learning_seed_service import LearningSeedService

YOUTUBE_URL_REGEX = re.compile(
    r'^https://(www\.)?(youtube\.com/(watch\?v=|playlist\?list=|results\?search_query=)|youtu\.be/)[a-zA-Z0-9_\-\.%\+=&]+$'
)

class YouTubeResourceService:
    """
    Manages YouTube learning resources organized around technical topics & technologies.
    All YouTube URLs are validated HTTPS links or search query URLs.
    """

    @staticmethod
    def validate_youtube_url(url: str) -> bool:
        if not url or not isinstance(url, str):
            return False
        parsed = urlparse(url.strip())
        if parsed.scheme != "https":
            return False
        domain = parsed.netloc.lower()
        if domain not in ["www.youtube.com", "youtube.com", "youtu.be"]:
            return False
        if any(bad in url.lower() for bad in ["fake", "dummy", "example"]):
            return False
        return bool(YOUTUBE_URL_REGEX.match(url.strip()))

    @staticmethod
    def build_search_url(query: str) -> str:
        return LearningSeedService.build_search_url(query)

    @classmethod
    def get_categories(cls) -> List[Dict[str, Any]]:
        return LearningSeedService.get_categories()

    @classmethod
    def get_all_topics_catalog(cls) -> List[Dict[str, Any]]:
        """
        Returns master catalog of technical learning topics with metadata, icons, and resource lists.
        """
        return LearningSeedService.get_master_catalog()

    @classmethod
    def get_topic_by_id(cls, topic_id: str) -> Optional[Dict[str, Any]]:
        catalog = cls.get_all_topics_catalog()
        tid = topic_id.lower().strip()
        for t in catalog:
            if t["id"] == tid or t["slug"] == tid or t["title"].lower() == tid:
                return t
        return None

    @classmethod
    def get_resources_for_topic(cls, topic: str, target_role: str = "Software Engineer", user_skill_level: str = "Intermediate") -> List[Dict[str, Any]]:
        catalog = cls.get_all_topics_catalog()
        t_lower = topic.lower().strip() if topic else ""
        matched_resources = []

        for t in catalog:
            if t_lower in t["id"].lower() or t_lower in t["slug"].lower() or t_lower in t["title"].lower() or any(t_lower in tag.lower() for tag in t.get("tags", [])):
                matched_resources.extend(t.get("resources", []))

        if not matched_resources:
            for t in catalog:
                if t["id"] in ["dsa", "javascript", "python", "sql", "system_design"]:
                    matched_resources.extend(t.get("resources", []))
                    break

        return matched_resources[:5]

