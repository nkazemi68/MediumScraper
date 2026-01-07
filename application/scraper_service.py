import asyncio
import json
import os
from typing import List, Dict

from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_exponential

from config import settings
from core.entities import UserData, PostData
from infrastructure.api.medium_api import MediumApi
from infrastructure.db.models.post import Post
from infrastructure.db.models.user import User
from infrastructure.repository import UserRepository, PostRepository
from infrastructure.utils.parsers import parse_user_about_to_text
from infrastructure.utils.post_mapper import extract_post_data
from infrastructure.utils.user_mapper import extract_user_data


class ScraperService:
    def __init__(self, db_session: Session):
        self.session = db_session
        self.api = MediumApi()
        self.user_repo = UserRepository(db_session)
        self.post_repo = PostRepository(db_session)
        self.progress_file = settings.PROGRESS_FILE
        self.target_users = settings.SCRAPE_TARGET_USERS


    def _load_progress(self) -> Dict:
        if os.path.exists(self.progress_file):
            with open(self.progress_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "collected_users": [],
            "completed_topics": [],
            "detailed_users": [],
            "posts_scraped_users": [],
            "followers_scraped_users": [],
            "full_content_scraped_users": []
        }

    def _save_progress(self, progress: Dict):
        with open(self.progress_file, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, max=30), reraise=True)
    async def _fetch_topic_authors_page(self, topic: str, after: str = "") -> Dict:
        return await self.api.get_topic_authors(topic, after_user_id=after)

    async def collect_users_from_topics(self, topics: List[str], progress: Dict):
        print(f"\nCollecting ALL users from {len(topics)} topics (no early stop)")

        all_unique_usernames = set()

        username_to_id = {}

        for topic in topics:
            if topic in progress["completed_topics"]:
                print(f"Topic '{topic}' already processed - skipping")
                continue

            print(f"\nFetching ALL users from topic: {topic}")
            after = ""
            topic_total = 0

            while True:
                try:
                    resp = await self._fetch_topic_authors_page(topic, after)
                    edges = resp[0]["data"]["recommendedPublishers"]["edges"]

                    if not edges:
                        print(f"No more users in topic {topic}")
                        break

                    for edge in edges:
                        node = edge["node"]
                        if node["__typename"] != "User":
                            continue

                        username = node["username"]
                        user_id = node.get("id")

                        if username not in all_unique_usernames:
                            all_unique_usernames.add(username)
                            if user_id:
                                username_to_id[username] = user_id
                            topic_total += 1

                    print(f"  Fetched page — {len(edges)} edges — {topic_total} users from this topic so far")

                    page_info = resp[0]["data"]["recommendedPublishers"]["pageInfo"]
                    if not page_info["hasNextPage"]:
                        break
                    after = page_info["endCursor"]

                    await asyncio.sleep(1.2)

                except Exception as e:
                    print(f"Error in topic {topic}: {e} - waiting 30 seconds...")
                    await asyncio.sleep(30)

            progress["completed_topics"].append(topic)
            self._save_progress(progress)
            print(f"Topic {topic} completed — {topic_total} new users collected")

        print(f"\nAll topics processed — Total unique users found: {len(all_unique_usernames)}")

        selected_usernames = list(all_unique_usernames)[:self.target_users]

        if len(selected_usernames) < self.target_users:
            print(f"Warning: Only {len(selected_usernames)} users available (target was {self.target_users})")

        progress["collected_users"] = selected_usernames

        print(f"Storing {len(selected_usernames)} selected users in database...")
        for username in selected_usernames:
            user_id = username_to_id.get(username)
            existing = self.session.query(User).filter(User.username == username).first()
            if not existing:
                self.session.add(User(id=user_id, username=username))

        self.session.commit()
        self._save_progress(progress)

        print(f"Collection phase completed!")
        print(f"Selected {len(selected_usernames)} users for further processing")

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, max=30), reraise=True)
    async def _fetch_user_details(self, username: str) -> Dict:
        return await self.api.get_user_data(username)

    async def scrape_user_details(self, username: str, progress: Dict):
        if username in progress["detailed_users"]:
            return

        print(f"Fetching details and about for user: @{username}")
        try:
            response = await self._fetch_user_details(username)
            user_raw = response[0]["data"]["userResult"]
            if user_raw["__typename"] != "User":
                return

            user_data: UserData = extract_user_data(response[0])
            _, about_text = parse_user_about_to_text(user_data.about)

            self.user_repo.save_or_update(user_data, about_text=about_text)

            progress["detailed_users"].append(username)
            self._save_progress(progress)
            print(f"Details for @{username} saved")

        except Exception as e:
            print(f"Error fetching details for @{username}: {e} - continuing")

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, max=30), reraise=True)
    async def _fetch_user_posts_page(self, username: str) -> Dict:
        return await self.api.get_user_posts(username)

    async def scrape_user_posts(self, username: str, progress: Dict):
        if username in progress["posts_scraped_users"]:
            return

        print(f"Fetching latest 10 posts for: @{username}")
        try:
            response = await self._fetch_user_posts_page(username)
            posts = response[0]["data"]["userResult"]["homepagePostsConnection"]["posts"][:10]

            for p in posts:
                post_data: PostData = extract_post_data(p)
                self.post_repo.save_or_update(post_data)

            progress["posts_scraped_users"].append(username)
            self._save_progress(progress)
            print(f"{len(posts)} posts saved for @{username}")

        except Exception as e:
            print(f"Error fetching posts for @{username}: {e} - continuing")

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, max=30), reraise=True)
    async def _fetch_full_post_content(self, post: Post) -> tuple:
        response = await self.api.get_full_post_content(post.id)
        return post, response

    async def scrape_full_post_contents(self, username: str, progress: Dict):
        if username in progress["full_content_scraped_users"]:
            return

        print(f"Fetching full content for posts of: @{username}")
        try:
            user = self.user_repo.get_by_username(username)
            if not user:
                return

            posts = user.posts.all()
            updated_posts = 0

            tasks = [self._fetch_full_post_content(post) for post in posts if not post.content]
            results = await asyncio.gather(*tasks, return_exceptions=False)

            for post, content in results:
                raw_content = content[0]["data"]["post"]["content"]["bodyModel"]
                post.content = json.dumps(raw_content)
                self.session.merge(post)
                updated_posts += 1

            if updated_posts > 0:
                self.session.commit()

            progress["full_content_scraped_users"].append(username)
            self._save_progress(progress)
            print(f"{updated_posts} posts updated with full content for @{username}")

        except Exception as e:
            print(f"Error fetching full content for posts of @{username}: {e} - continuing")

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=2, max=30), reraise=True)
    async def _fetch_followers_page(self, username: str, from_cursor: str = None) -> Dict:
        return await self.api.get_user_followers(username, followers_from=from_cursor)

    async def scrape_user_followers(self, username: str, progress: Dict):
        if username in progress["followers_scraped_users"]:
            return

        user = self.user_repo.get_by_username(username)
        if not user or user.followers_count == 0:
            progress["followers_scraped_users"].append(username)
            self._save_progress(progress)
            return

        print(f"Fetching {user.followers_count} followers for @{username}")
        from_cursor = None
        total_saved = 0

        while total_saved < 30:
            try:
                response = await self._fetch_followers_page(username, from_cursor)
                followers = response[0]["data"]["userResult"]["followersUserConnection"]["users"]
                print(f"fetched {len(followers)} number of {username} followers")

                for follower_data in followers:
                    print(f"total followers saved: {total_saved}")
                    if total_saved >= 30:
                        break
                    follower_exists = self.session.query(User).filter(User.id == follower_data["id"]).first()
                    if follower_data["__typename"] == "User" and not follower_exists:
                        follower = User(
                            id=follower_data["id"],
                            username=follower_data["username"],
                            name=follower_data.get("name"),
                            bio=follower_data.get("bio")
                        )
                        self.session.add(follower)

                        if user not in follower.following:
                            follower.following.append(user)

                        total_saved += 1

                self.session.commit()
                next_page_info = response[0]["data"]["userResult"]["followersUserConnection"]["pagingInfo"].get("next")
                if not next_page_info or not next_page_info.get("from"):
                    break
                from_cursor = next_page_info["from"]

                await asyncio.sleep(1)

            except Exception as e:
                print(f"Error fetching followers for @{username}: {e} - waiting 10 seconds...")
                await asyncio.sleep(10)

        progress["followers_scraped_users"].append(username)
        self._save_progress(progress)
        self.session.commit()
        print(f"{total_saved} followers saved for @{username}")

    async def all_in_one(self, topics: List[str]):
        progress = self._load_progress()
        print(f"Starting full scrape - target: {self.target_users} users")
        print(f"So far {len(progress['collected_users'])} users collected")

        await self.collect_users_from_topics(topics, progress)

        for username in progress["collected_users"]:
            await self.scrape_user_details(username, progress)
            await self.scrape_user_posts(username, progress)
            await self.scrape_full_post_contents(username, progress)
            await self.scrape_user_followers(username, progress)

            self.session.commit()

        print("\nScraping completed! Everything saved and resilient to errors.")
        print(f"Progress file: {self.progress_file}")