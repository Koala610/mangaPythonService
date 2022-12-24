from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, LargeBinary

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255))
    bookmarks_hash = Column(BigInteger)
    bookmarks_per_page = Column(Integer, default=10)
    technical_info = Column(LargeBinary)
    is_subscribed = Column(Boolean, default=False)
