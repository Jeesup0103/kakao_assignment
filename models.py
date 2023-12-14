from sqlalchemy import Column, Integer, String, ForeignKey
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

class ChatList(Base):
    __tablename__ = "chatlist"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.index'))
    chat_id = Column(Integer, ForeignKey('chats.index'))
    
class Friend(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('users.index'))
    friendname = Column(String, ForeignKey('users.index'))
