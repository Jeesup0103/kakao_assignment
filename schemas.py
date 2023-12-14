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
    username: str
    password: str


class UserRequestCreate(UserRequestBase):
    pass


class UserRequest(UserRequestBase):
    index: Optional[int]

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        
class AddFriendRequest(BaseModel):
    username: str