from dataclasses import dataclass
from typing import Optional, Dict, List, Any


@dataclass
class TopicData:
    topic_id: str
    title: str


@dataclass
class UserData:
    user_id: str
    username: str
    name: Optional[str] = None
    bio: Optional[str] = None

    image_id: Optional[str] = None
    subdomain: Optional[str] = None
    is_book_author: bool = False
    membership_data: Optional[Dict[str, str]] = None

    follower_count: int = 0
    following_count: int = 0

    user_meta: Optional[Dict[str, str]] = None

    about: Optional[Any] = None


@dataclass
class PostData:
    post_id: str
    author_id: str
    title: str
    published_at: str
    subtitle: Optional[str] = None
    clap_count: Optional[int] = None
    responses_count: Optional[int] = None
    reading_time: Optional[float] = None
    collection_id: Optional[int] = None
    content: Optional[Dict] = None


@dataclass
class FollowerData:
    user_id: str
    followed_user_id: str
