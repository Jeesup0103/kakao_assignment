from sqlalchemy.orm import Session

from models import Chat, User, Friend, ChatList
from schemas import ChatRequest, UserRequest

import logging


def get_chat(db: Session, chat_id:int):
    return db.query(Chat).filter(Chat.chatlist_id == chat_id).all()


def add_chat(db: Session, item: ChatRequest) -> Chat:
    # Create a new Chat model instance from the provided schema
    new_chat = Chat(name=item.name, text=item.text, date=item.date, chatlist_id = item.chatlist_id)

    # Add the new chat message to the session and commit the transaction
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return db.query(Chat).all()


def create_user(db: Session, user_data: UserRequest) -> User:
    new_user = User(username=user_data.username, password=user_data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_friendship(db: Session, username: str, friendname: str):
    new_friend = Friend(username=username, friendname=friendname)
    opposite_new_friend = Friend(username=friendname, friendname=username)

    db.add(new_friend)
    db.add(opposite_new_friend)
    db.commit()

    db.refresh(new_friend)
    db.refresh(opposite_new_friend)
    
def create_chat(db: Session, user1: User, user2: User):
    new_chat = ChatList()
    new_chat.users.append(user1)
    new_chat.users.append(user2)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat