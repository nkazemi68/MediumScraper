from sqlalchemy import create_engine
from base import Base
from config import settings
from models.user import User
from models.post import Post
from models.topic import Topic


engine = create_engine(settings.DATABASE_URL)

def create_db_tables():
    Base.metadata.create_all(bind=engine)
    print("database and tables created successfully")