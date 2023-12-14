from fastapi import FastAPI, Depends, Request, WebSocket, HTTPException, Response
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from schemas import ChatRequest, ChatRequestCreate, UserRequest, UserRequestCreate, UserResponse, AddFriendRequest
from crud import get_chat, add_chat, create_user, create_friendship
from models import Base, Chat, User, Friend
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm

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

@app.get("/chat")
def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
def get_index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/friends")
def get_index(request: Request):
    return templates.TemplateResponse("friends.html", {"request": request})

@app.get("/getchat", response_model=List[ChatRequest])
def get_data(db: Session = Depends(get_db)):
    return get_chat(db)


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
def add_friend(request: AddFriendRequest, db: Session = Depends(get_db), current_user: User =Depends(login_manager)):
    friend_user = db.query(User).filter(User.username == request.username).first()

    if not friend_user:
        raise HTTPException(status_code=404, detail="Friend not found")
    create_friendship(db, current_user.username, friend_user.username)
    return {"message": "Friend successfully registered"}
   