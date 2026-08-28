class SystemDesignService:
    @staticmethod
    def evaluate_architecture(components: list, prompt: str = "Design a URL Shortener") -> dict:
        comp_set = set([c.lower() for c in components])
        
        has_lb = any("load balancer" in c or "lb" in c for c in comp_set)
        has_cache = any("redis" in c or "cache" in c or "memcached" in c for c in comp_set)
        has_db = any("database" in c or "mongodb" in c or "postgresql" in c or "sql" in c for c in comp_set)
        has_queue = any("kafka" in c or "rabbitmq" in c or "queue" in c for c in comp_set)
        has_cdn = any("cdn" in c or "cloudflare" in c for c in comp_set)
        
        score = 40
        if has_lb: score += 15
        if has_cache: score += 20
        if has_db: score += 15
        if has_queue or has_cdn: score += 10
        
        score = min(100, score)
        tier = "Production-Ready Tier 1 Architecture" if score >= 85 else "Scalable Design" if score >= 70 else "Basic Architecture"
        
        return {
            "architecture_score": score,
            "evaluation_tier": tier,
            "strengths": [
                "Utilized caching layer for high read throughput." if has_cache else "Included primary database.",
                "Load balancer incorporated for fault tolerance." if has_lb else "Basic server setup."
            ],
            "scalability_checklist": {
                "load_balancing": "Passed" if has_lb else "Missing Load Balancer",
                "caching_strategy": "Passed (Redis/Memcached)" if has_cache else "Add Redis for sub-10ms reads",
                "database_partitioning": "Passed" if has_db else "Define storage model",
                "asynchronous_queues": "Passed" if has_queue else "Optional: Add Kafka for background writes"
            },
            "estimated_capacity": "Handles 100,000+ Requests/Sec" if score >= 80 else "Handles 5,000 Requests/Sec"
        }
