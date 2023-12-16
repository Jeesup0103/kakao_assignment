# SKKU Talk

웹프로그래밍실습 파이널 과제

## Framework, Stack

- fastapi
- sqlite
- Jinja template
- sqlalchemy

## Installation

> pip install -r requirements.txt

## Code Structure
assets 폴더에서 이미지와 동영상의 저장을 관리한다. static 폴더에서 js 파일들과 css 파일을 관리한다. templates 폴더에서 html 파일들을 관리한다.

- crud.py

DB에서 읽거나 쓰는 함수들을 관리하는 파일이다.
- database.py

DB 설정 파일이다.
- main.py

API 관리와 웹소켓 관리를 하는 파일이다.
- models.py

DB 구조를 관리하는 파일이다.

- schemas.py

DB 스키마를 통해 request와 response를 돕는 파일이다.

## DB Diagram
![alt text](https://github.com/Jeesup0103/kakao_assignment/tree/main/md-image/diagram.png?raw=true)

## How to run

> uvicorn main:app

### 시작 화면

> http://127.0.0.1:8000/login

## Basic Features

### Login

> http://127.0.0.1:8000/login

아이디와 비밀번호를 입력해서 register 버튼을 눌러서 DB에 사용자를 등록한다.

다시 아이디와 비밀번호를 입력해서 login 버튼을 눌러서 friendlist 페이지로 이동한다.

### Friend List

> http://127.0.0.1:8000/friends

가장 위에 friendlist title이 보이고 그 밑에 로그인된 유저의 아이디가 보인다.

그 밑에 노란색 버튼은 친구 추가 버튼으로 해당 버튼을 누르면 prompt로 추가하고 싶은 친구의 이름을 추가 할 수 있다.

추가하고 싶은 친구는 DB에 저장되어 있는 유저의 아이디여야 한다.

그 밑으로 로그인된 유저와 친구인 유저들의 아이디가 나열되어있다.

해당 친구와 1대1 대화를 진행하고 싶을 때 해당 친구를 눌러 1대1 채팅방으로 이동한다.

### 1 to 1 Chatting

> http://127.0.0.1:8000/chat/{chat_id}

해당 친구와의 채팅 기록이 있다면 불러오게 되고 아니면 새로 시작하게 된다.

상단 좌측에 뒤로가기 버튼으로 다시 friendlist 페이지로 갈 수 있다.

채팅이 많으면 scroll을 통해 채팅을 살펴 볼 수 있다.

상대방의 채팅을 이름과 그 밑에 메세지 혹은 미디어와 보낸 시간이 있다.

그 밑에 흰색 부분에서 채팅을 입력해 send 버튼 혹은 키보드에서 엔터를 누르면 메세지를 보낼 수 있다.

두개의 브라우저를 열어 다른 유저로 로그인 한 후 같은 1대1 채팅을 하면 웹소켓으로 메세지가 전송되고 받아지는 것을 볼 수 있다.

### Chat List

> http://127.0.0.1:8000/chatlist

friend list 페이지에서 하단에 Chats 버튼을 클릭하면 chat list 페이지로 이동 할 수 있다.

상단에 Chat list라고 제목이 나와 있고 그 밑에 로그인 된 유저의 아이디를 볼 수 있다.

그 밑으로 로그인 된 유저와 채팅을 하고 있는 다른 유저들의 이름과 가장 최근에 이루어진 채팅을 확인 할 수 있다.

해당 채팅을 누르게 되면 그 친구와 1대1 채팅을 할 수 있다.

## Additional Features

### Sending and Viewing Photo in Chatting room

> http://127.0.0.1:8000/chat/{chat_id}

이미지 전송은 친구와의 채팅 방에서 이루어진다. 아무 친구를 선택해 대화방에 입장을 한다.

화면 하단 좌측에 '+' 버튼을 누르면 파일 선택과 미디어 업로드 버튼이 나온다.

이미지 파일을 선택해 미디어 업로드 버튼을 누르면 이미지가 친구에게 전송되는 것을 볼 수 있다.

위의 1대1 채팅에서의 기능과 마찬가지로 다른 유저로 로그인 한 브라우저에서 웹소켓으로 메세지가 받아지는 것을 볼 수 있다.

해당 이미지를 클릭하면 다른 탭에서 이미지 전체를 볼 수 있다. 이미지를 다운 받을 수도 있다.

이미지는 assets/image 폴더 안에 저장되고 해당 이미지의 경로가 DB에 저장된다.

### Sending and Viewing Video in Chatting room

> http://127.0.0.1:8000/chat/{chat_id}

동영상 전송은 친구와의 채팅 방에서 이루어진다. 아무 친구를 선택해 대화방에 입장을 한다.

화면 하단 좌측에 '+' 버튼을 누르면 파일 선택과 미디어 업로드 버튼이 나온다.

동영상 파일을 선택해 미디어 업로드 버튼을 누르면 동영상이 친구에게 전송되는 것을 볼 수 있다.

위의 1대1 채팅에서의 기능과 마찬가지로 다른 유저로 로그인 한 브라우저에서 웹소켓으로 메세지가 받아지는 것을 볼 수 있다.

해당 동영상은 html5 video controls를 이용했기 때문에 동영상 재생과 전체화면 등의 기능을 갖고 있다. 그래서 동영상 재생을 누르면 해당 동영상이 재생되는 것을 볼 수 있다.

동영상은 asstes/video 폴더 안에 저장되고 해당 동영상의 경로가 DB에 저장된다.
