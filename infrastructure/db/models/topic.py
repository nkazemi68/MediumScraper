from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db.base import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(String, primary_key=True)

    display_title = Column(String, nullable=False)
    normalized_slug = Column(String, unique=True, nullable=False, index=True)

    parent_id = Column(String, ForeignKey("topics.id"), nullable=True)

    children = relationship("Topic", back_populates="parent", lazy="dynamic")

    parent = relationship("Topic", remote_side=[id], back_populates="children")  # type: ignore[arg-type]

    def __repr__(self):
        return f"<Topic {self.display_title} ({self.normalized_slug})>"