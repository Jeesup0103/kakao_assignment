from pydantic import BaseModel
from typing import Optional


class ChatRequestBase(BaseModel):
    chatlist_id:Optional[int]
    name: str
    text: str
    date: str


class ChatRequestCreate(ChatRequestBase):
    pass


class ChatRequest(ChatRequestBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class UserRequestBase(BaseModel):
    username: str
    password: str


class UserRequestCreate(UserRequestBase):
    pass


class UserRequest(UserRequestBase):
    id: Optional[int]

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        
class AddFriendRequest(BaseModel):
    username: str
    