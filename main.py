from fastapi import FastAPI, Depends, Request, WebSocket, HTTPException, Response, UploadFile, File, Form
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from schemas import ChatRequest, ChatRequestCreate, UserRequest, UserRequestCreate, UserResponse, AddFriendRequest
from crud import get_chat, add_chat, create_user, create_friendship, create_chat
from models import Base, Chat, User, Friend, ChatList
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm
import json

import logging

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class NotAuthenticatedException(Exception):
    pass


app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")

SECRET = "secret"
login_manager = LoginManager(
    SECRET, "/login", use_cookie=True, custom_exception=NotAuthenticatedException
)


@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exec: NotAuthenticatedException):
    return RedirectResponse(url="/login")


def user_loader(username: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        return user
    finally:
        db.close()


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{data}")
    except Exception as e:
        pass
    finally:
        await manager.disconnect(websocket)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            await manager.broadcast(f"{data}")
    except Exception as e:
        pass
    finally:
        await manager.disconnect(websocket)


manager = ConnectionManager()

@app.get("/chat/{chat_id}")
def get_chat_page(request: Request, chat_id:int):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/login")
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/friends")
def get_friends_page(request: Request):
    return templates.TemplateResponse("friends.html", {"request": request})

@app.get("/chatlist")
def get_chatlists_page(request: Request):
    return templates.TemplateResponse("chatlist.html", {"request": request})


@app.get("/getchat/{chat_id}", response_model=List[ChatRequest])
def get_data(chat_id:int, db: Session = Depends(get_db)):
    return get_chat(db, chat_id)

@app.post("/postchat", response_model=List[ChatRequest])
def post_chat(chat_req: ChatRequestCreate, db: Session = Depends(get_db)):
    return add_chat(db, chat_req)

@app.post("/token")
def login(
    response: Response,
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    username = data.username
    password = data.password
    user = user_loader(username)

    if not user or user.password != password:
        raise InvalidCredentialsException
    access_token = login_manager.create_access_token(data={"sub": username})
    login_manager.set_cookie(response, access_token)
    login_manager.user_loader(user_loader)
    return {"access_token": access_token}

@app.post("/register")
def register(response: Response, user_request: UserRequestCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user_request)
    access_token = login_manager.create_access_token(data={"sub": new_user.username})
    login_manager.set_cookie(response, access_token)

    return {"message": "User successfully registered", "access_token": access_token}

@app.get("/logout")
def logout(response: Response):
    response=RedirectResponse("/login", status_code=302)
    response.delete_cookie(key="access-token")
    return response

@app.get("/get-username")
def get_username(current_user: User = Depends(login_manager)):
    return current_user.username

@app.get("/get-friends")
def get_friends(db: Session = Depends(get_db), current_user: User = Depends(login_manager)):
    # Query for the current user's friends
    friends = db.query(Friend).filter(Friend.username == current_user.username).all()

    # Retrieve friend details
    friend_usernames = []
    for friend in friends:
        friend_usernames.append(friend.friendname)

    return friend_usernames

@app.post("/add-friend")
def add_friend(request: AddFriendRequest, db: Session = Depends(get_db), current_user: User = Depends(login_manager)):
    friend_user = db.query(User).filter(User.username == request.username).first()

    if not friend_user:
        raise HTTPException(status_code=404, detail="Friend not found")
    create_friendship(db, current_user.username, friend_user.username)
    return {"message": "Friend successfully registered"}
   
@app.get("/get-one-chat")
def get_one_chat(user1: str, user2: str, db: Session = Depends(get_db)):
    # Find User based on usernames
    user1_obj = db.query(User).filter(User.username == user1).first()
    user2_obj = db.query(User).filter(User.username == user2).first()

    if not user1_obj or not user2_obj:
        raise HTTPException(status_code=404, detail="User not found")

    chat = db.query(ChatList).filter(
        (ChatList.user1 == user1_obj.username) & (ChatList.user2 == user2_obj.username)
    ).first()

    if not chat:
        chat = db.query(ChatList).filter(
            (ChatList.user1 == user2_obj.username) & (ChatList.user2 == user1_obj.username)
        ).first()
    if not chat:
        create_chat(db, user1_obj, user2_obj)
        chat = db.query(ChatList).filter(
            (ChatList.user1 == user1_obj.username) & (ChatList.user2 == user2_obj.username)
        ).first()

    return chat

@app.get("/get-chatlist")
def get_chat_list(db: Session = Depends(get_db), current_user: User = Depends(login_manager)):
    # Query to find chat lists involving the current user
    chat_lists = db.query(
        ChatList.id,
        ChatList.user1,
        ChatList.user2,
        Chat.text,
        func.max(Chat.date).label("latest_date")
    ).join(Chat, ChatList.id == Chat.chatlist_id)\
    .filter((ChatList.user1 == current_user.username) | (ChatList.user2 == current_user.username))\
    .group_by(ChatList.id, ChatList.user1, ChatList.user2)\
    .order_by(desc("latest_date"))\
    .all()

    # Process the query results
    results = []
    for chat_id, user1, user2, latest_text, _ in chat_lists:
        opponent_user = user1 if user1 != current_user.username else user2
        results.append({
            "chat_id": chat_id,
            "opponent_username": opponent_user,
            "latest_message": latest_text
        })

    return results

@app.post("/upload-media")
async def upload_media(chatlist_id: int = Form(...), date: str = Form(...), media: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(login_manager)):
    file_location = f"assets/{'image' if 'image' in media.content_type else 'video'}/{media.filename}"
    with open(file_location, "wb") as file_object:
        file_object.write(await media.read())

    # Assuming you have a method to determine the type (image or video) and set the appropriate URL
    image_url = file_location if 'image' in media.content_type else None
    video_url = file_location if 'video' in media.content_type else None

    # Save the media URL and other details in the database
    new_chat = Chat(chatlist_id=chatlist_id, date=date, image_url=image_url, video_url=video_url, name=current_user.username)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return new_chat