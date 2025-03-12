from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)


class LogEntry(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
