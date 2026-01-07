import json
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from core.entities import UserData, PostData
from infrastructure.db.models.post import Post
from infrastructure.db.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()

    def save_or_update(self, user_data: UserData) -> User:
        user = self.get_by_username(user_data.username)
        if not user:
            user = User(
                id=user_data.user_id,
                username=user_data.username
            )
            self.session.add(user)

        user.name = user_data.name
        user.bio = user_data.bio
        user.image_id = user_data.image_id
        user.subdomain = user_data.subdomain
        user.is_book_author = user_data.is_book_author
        user.followers_count = user_data.follower_count
        user.following_count = user_data.following_count
        user.user_meta = json.dumps(user_data.user_meta)
        user.about = user_data.about

        self.session.commit()
        return user

    def add(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()


class PostRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, post_id: str) -> Optional[Post]:
        return self.session.query(Post).filter(Post.id == post_id).first()

    def save_or_update(self, post_data: PostData) -> Post:
        post = self.get_by_id(post_data.post_id)
        if not post:
            post = Post(id=post_data.post_id, author_id=post_data.author_id)
            self.session.add(post)

        post.title = post_data.title
        post.published_at = datetime.fromtimestamp(int(post_data.published_at) / 1000)
        post.subtitle = post_data.subtitle
        post.clap_count = post_data.clap_count
        post.responses_count = post_data.responses_count
        post.reading_time = post_data.reading_time
        post.collection_id = post_data.collection_id

        self.session.commit()

        return post

    def bulk_save(self, posts: List[Post]) -> None:
        self.session.bulk_save_objects(posts)
        self.session.commit()
