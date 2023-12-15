from sqlalchemy import Column, Integer, String, ForeignKey, Table
from database import Base
from sqlalchemy.orm import relationship

# Association table
chat_user_link = Table('chat_user_link', Base.metadata,
    Column('chat_id', Integer, ForeignKey('chatlist.id')),
    Column('username', Integer, ForeignKey('users.username'))
)

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String)
    date = Column(String)
    chatlist_id = Column(Integer, ForeignKey('chatlist.id')) 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    chats = relationship('ChatList', secondary=chat_user_link)

class ChatList(Base):
    __tablename__ = "chatlist"
    id = Column(Integer, primary_key=True)
    users = relationship('User', secondary=chat_user_link)
    
class Friend(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    username = Column(String, ForeignKey('users.username'))
    friendname = Column(String, ForeignKey('users.username'))
