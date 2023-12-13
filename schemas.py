from pydantic import BaseModel
from typing import Optional


class ChatRequestBase(BaseModel):
    name: str
    text: str
    date: str


class ChatRequestCreate(ChatRequestBase):
    pass


class ChatRequest(ChatRequestBase):
    index: Optional[int]

    class Config:
        orm_mode = True


class UserRequestBase(BaseModel):
    userId: str
    password: str


class UserRequestCreate(UserRequestBase):
    pass


class UserRequest(UserRequestBase):
    index: Optional[int]

    class Config:
        orm_mode = True
