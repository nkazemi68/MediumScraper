"""
Main entry point of the application

CLI execution:
    python main.py
    python main.py --topics startups python --target-users 200
    python main.py --reset

FastAPI execution (in the future):
    python main.py --mode api
"""

from interfaces.cli.cli import create_parser, run_scraper
import sys


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    topics = args.topics

    if args.mode == "scrape":
        run_scraper(args.topics, args.target_users, args.reset)
    elif args.mode == "api":
        print("FastAPI not yet implemented — coming soon!")
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)