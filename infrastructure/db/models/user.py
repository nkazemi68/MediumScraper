from sqlalchemy import Column, String, Integer, Table, Text, BigInteger, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from infrastructure.db.base import Base


followers = Table(
    "followers",
    Base.metadata,  # یا Base.metadata
    Column("follower_id", String, ForeignKey("users.id"), primary_key=True),
    Column("followed_id", String, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)

    image_id = Column(String, nullable=True)
    subdomain = Column(String, nullable=True)
    is_book_author = Column(Boolean, default=False)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)

    user_meta = Column(JSONB, nullable=True)

    about = Column(Text, nullable=True)

    following = relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref="followers",
        lazy="dynamic"
    )

    posts = relationship("Post", back_populates="author", lazy="dynamic")

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(followers.c.followed_id == user.id).count() > 0