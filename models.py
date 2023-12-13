from sqlalchemy import Column, Integer, String
from database import Base


class Chat(Base):
    __tablename__ = "chats"
    index = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String)
    date = Column(String)


class User(Base):
    __tablename__ = "users"
    index = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
