from fastapi import FastAPI, Depends, Request, WebSocket, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from schemas import ChatRequest, ChatRequestCreate, UserRequest, UserRequestCreate
from crud import get_chat, add_chat, create_user
from models import Base, Chat, User
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import logging

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")


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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.userId == username).first()
    db.close()
    if (
        user and user.password == password
    ):  # Replace this line with hashed password check if necessary
        return True
    else:
        return False


@app.get("/")
def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/loginpage")
def get_index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/getchat", response_model=List[ChatRequest])
def get_data(db: Session = Depends(get_db)):
    return get_chat(db)


@app.post("/postchat", response_model=List[ChatRequest])
def post_chat(chat_req: ChatRequestCreate, db: Session = Depends(get_db)):
    return add_chat(db, chat_req)


@app.post("/login")
async def login(username: str, password: str):
    if verify_user(username, password):
        # Logic for successful login
        return {"message": "Login successful"}


@app.post("/register", response_model=List[UserRequest])
def register(user_request: UserRequestCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user_request)
    logging.warning(f"New user data: {user_request}")
    return new_user
