from sqlalchemy import Column, Integer, String, ForeignKey, Table
from database import Base
from sqlalchemy.orm import relationship


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String)
    date = Column(String)
    image_url=Column(String, nullable=True)
    video_url=Column(String, nullable=True)
    chatlist_id = Column(Integer, ForeignKey('chatlist.id')) 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

class ChatList(Base):
    __tablename__ = "chatlist"
    id = Column(Integer, primary_key=True)
    user1 = Column(String, ForeignKey("users.username"))
    user2 = Column(String, ForeignKey("users.username"))
    
class Friend(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    username = Column(String, ForeignKey('users.username'))
    friendname = Column(String, ForeignKey('users.username'))
