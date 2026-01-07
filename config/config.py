from dotenv import load_dotenv
from os import environ
from typing import List

load_dotenv()


class Settings:
    DATABASE_URL: str = environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:password@localhost:5432/medium_scraper"
    )
    PROXY_LIST: List[str] = [
                                p.strip() for p in environ.get("PROXY_LIST", "").split(",") if p.strip()
                            ] or None
    REQUEST_TIMEOUT: int = int(environ.get("REQUEST_TIMEOUT", "10"))
    SCRAPE_TARGET_USERS: int = int(environ.get("SCRAPE_TARGET_USERS", "100"))
    PROGRESS_FILE: str = environ.get("PROGRESS_FILE", "scraper_progress.json")


settings = Settings()
