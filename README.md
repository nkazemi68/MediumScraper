# MediumScraper

A professional, resilient, and modular web scraper for Medium.com built with Clean Architecture principles in Python.

This project automatically collects:
- Unique users from multiple Medium topics
- User details and "About" section
- Latest 10 posts per user
- Full post content
- All followers for each user (with relationship modeling)

Data is stored in PostgreSQL using SQLAlchemy ORM, with resume capability via `scraper_progress.json`.

## Features

- **Clean Architecture** (core, application, infrastructure, interfaces)
- **Fully automatic & resilient** — retries on errors, graceful interrupt handling (Ctrl+C saves progress)
- **Resume support** — continues from where it left off
- **Unique user collection** — collects all users from topics, then selects target number
- **Follower/Following relationship** — proper many-to-many modeling
- **Configurable via `.env`**
- **CLI-driven** (FastAPI support planned)

## Project Structure

```tree
MediumScraper/
├── application/              # Business logic (ScraperService)
├── core/                     # Entities and domain models
├── infrastructure/
│   ├── api/                  # Medium API client
│   ├── db/
│   │   ├── models/           # SQLAlchemy models (User, Post, etc.)
│   │   ├── base.py
│   │   └── create_db.py
│   ├── utils/                # Parsers and mappers
│   └── repository.py         # Repository pattern for DB operations
├── interfaces/cli/           # Command-line interface
├── config/                   # Configuration (.env loading)
├── main.py                   # Main entry point
├── topics.json               # Topic slugs mapping (display title → slug)
├── scraper_progress.json     # Auto-generated progress file (do not delete manually unless resetting)
└── .env                      # Your environment variables (create from .env.example)
```

## Prerequisites

- Python 3.10+
- PostgreSQL (local or remote)
- Git

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/MediumScraper.git
cd MediumScraper
```

2. **Create a virtual environment**


```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

Note: If requirements.txt is not present yet, install the main ones:
```bash
pip install sqlalchemy psycopg2-binary python-dotenv tenacity curl-cffi asyncio
```

4. **Set up PostgreSQL**

Install PostgreSQL locally or use a remote server.
Create a new database (e.g., medium_scraper):

```sql
CREATE DATABASE medium_scraper;
```

5. **Configure `.env`**

Copy the example and fill in your details:
```bash
cp .env.example .env
```

Edit .env:

```env
DATABASE_URL=postgresql+psycopg2://your_username:your_password@localhost:5432/medium_scraper
PROXY_LIST=            # Optional: comma-separated proxies, e.g. http://ip:port,http://ip2:port
REQUEST_TIMEOUT=30
SCRAPE_TARGET_USERS=100
PROGRESS_FILE=scraper_progress.json
```

6. **Topic Slugs**

The file topics.json contains mapping from display titles to actual Medium slugs.
Example content:
```json
{
  "Tech Companies": "tech-companies",
  "Artificial Intelligence": "artificial-intelligence",
  "Data Science": "data-science",
  "Programming": "programming",
  "DevOps": "devops",
  "Charter Schools": "charter-schools",
  "Startups": "startup"
}
```

You can modify this file to add/remove/changetopics.

## Running the Scraper
The scraper runs via CLI using `main.py`.

## Common Commands

```bash
# Default run: continue from previous progress with default topics and target 100
python main.py

# Start fresh (delete previous progress)
python main.py --reset

# Custom topics and target
python main.py --topics startup programming artificial-intelligence --target-users 200

# Start from scratch with custom settings
python main.py --reset --topics tech-companies data-science --target-users 50

# Show help
python main.py --help
```

## Default Values

- Topics: `tech-companies`, `artificial-intelligence`, `data-science`, `programming`, `devops`, `charter-schools`, `startup`
- Target users: `100` (configurable in `.env` as `SCRAPE_TARGET_USERS`)
- Progress file: `scraper_progress.json`

## What Happens on First Run

- Tables are automatically created in your PostgreSQL database
- Users are collected from all topics
- Unique users are selected up to the target number
- Details, posts, and followers are scraped
- Progress is saved continuously

## Interrupt & Resume
### Press Ctrl+C at any time:

- Progress is saved automatically
- Next run (`python main.py`) will resume from where it left off

### Use `--reset` only if you want to start completely over.

## Future Plans

- FastAPI endpoint to view scraped data (--mode api)
- Full post content scraping
- Dashboard/UI
- Docker support
- Rate limit handling improvements

## License

### MIT License — see LICENSE file.

---

### Made with ❤️ for learning, automation, and clean code.