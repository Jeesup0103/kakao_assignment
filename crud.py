from sqlalchemy.orm import Session

from models import Chat, User
from schemas import ChatRequest, UserRequest

import logging


def get_chat(db: Session):
    return db.query(Chat).all()


def add_chat(db: Session, item: ChatRequest) -> Chat:
    # Create a new Chat model instance from the provided schema
    new_chat = Chat(name=item.name, text=item.text, date=item.date)

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
