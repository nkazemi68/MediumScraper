# interfaces/cli/cli.py
import argparse
import os
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.scraper_service import ScraperService
from config import settings
from infrastructure.db.base import Base


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Medium Scraper — Automatically collect users, posts, and followers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--topics",
        nargs="+",
        default=[
            'tech-companies',
            'artificial-intelligence',
            'data-science',
            'programming',
            'devops',
            'charter-schools',
            'startup'
        ],
        help="List of topics to collect users from"
    )

    parser.add_argument(
        "--target-users",
        type=int,
        default=settings.SCRAPE_TARGET_USERS,
        help="Target number of unique users"
    )

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Start from scratch (delete previous progress)"
    )

    parser.add_argument(
        "--mode",
        choices=["scrape", "api"],
        default="scrape",
        help="Execution mode: scrape or api (coming soon)"
    )

    return parser


def run_scraper(topics: List[str], target_users: int, reset: bool):
    if reset and os.path.exists(settings.PROGRESS_FILE):
        print("Deleting previous progress...")
        os.remove(settings.PROGRESS_FILE)

    print(f"Starting automated scrape — target: {target_users} users")
    print(f"Topics: {', '.join(topics)}")

    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    scraper = ScraperService(session)
    scraper.target_users = target_users

    try:
        import asyncio
        asyncio.run(scraper.all_in_one(topics))
    except KeyboardInterrupt:
        print("\nScrape stopped — progress has been saved.")
    finally:
        session.close()
        print("Done! Progress file:", settings.PROGRESS_FILE)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    if args.mode == "scrape":
        run_scraper(args.topics, args.target_users, args.reset)
    elif args.mode == "api":
        print("Launching FastAPI... (coming soon!)")
        # uvicorn.run(app, host="0.0.0.0", port=8000)