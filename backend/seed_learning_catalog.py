import asyncio
import os
import sys

# Ensure backend path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.database.mongodb import db_manager
from app.services.learning_seed_service import LearningSeedService
from app.repositories.learning_repository import learning_repository

async def seed_learning_catalog():
    print("=" * 70)
    print("CAREER COPILOT: SEEDING TECHNICAL LEARNING CATALOG INTO MONGODB")
    print("=" * 70)

    try:
        await db_manager.connect()
        master_catalog = LearningSeedService.get_master_catalog()
        print(f"Master Catalog Loaded: {len(master_catalog)} Topics.")

        topics_col = learning_repository.topics_col
        resources_col = learning_repository.resources_col

        seeded_topics_count = 0
        seeded_resources_count = 0

        for topic in master_catalog:
            t_doc = dict(topic)
            resources = t_doc.pop("resources", [])

            # Upsert Topic
            await topics_col.update_one(
                {"id": t_doc["id"]},
                {"$set": t_doc},
                upsert=True
            )
            seeded_topics_count += 1

            # Upsert Subtopic Resources
            for res in resources:
                r_doc = dict(res)
                await resources_col.update_one(
                    {"id": r_doc["id"]},
                    {"$set": r_doc},
                    upsert=True
                )
                seeded_resources_count += 1

            print(f"  [OK] Seeded '{t_doc['title']}' ({len(resources)} subtopic resources)")

        print("-" * 70)
        print(f"SUCCESS: Seeded {seeded_topics_count} Topics and {seeded_resources_count} Subtopic Resources into MongoDB!")
        print("=" * 70)

    except Exception as e:
        print(f"ERROR Seeding Learning Catalog: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(seed_learning_catalog())
