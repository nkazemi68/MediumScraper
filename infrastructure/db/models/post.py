from sqlalchemy import Column, String, Integer, Table, Text, BigInteger, Boolean, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from infrastructure.db.base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)
    author_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    title = Column(String, nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    subtitle = Column(String, nullable=True)
    clap_count = Column(Integer, default=0)
    responses_count = Column(Integer, default=0)
    reading_time = Column(Numeric(precision=5, scale=2), default=0.00)
    collection_id = Column(String, nullable=True)
    content = Column(JSONB, nullable=True)

    author = relationship("User", back_populates="posts")
