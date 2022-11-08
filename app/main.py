import os
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, Response
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from config import ACCESS_TOKEN_EXPIRE, ALGORITHM, JWT_SIGNING_KEY
from schemas import Player, Lobby, PositionUpdate, PlayerBase
from sql import crud
from sql.database import Base, engine, SessionLocal
from token_form import TokenGetter

Base.metadata.create_all(bind=engine)
app = FastAPI()
token_getter = TokenGetter()


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(db: Session, username: str):
    player = crud.create_player(db, username)
    to_encode = {"id": player.id, "exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRE}
    encoded_jwt = jwt.encode(to_encode, JWT_SIGNING_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_player(token: str = Depends(token_getter), db: Session = Depends(get_db)) -> Player:
    def exception(detail: str = "Invalid authentication credentials"):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"authorization": "token"},
        )

    try:
        payload = jwt.decode(token, JWT_SIGNING_KEY, algorithms=[ALGORITHM])
        player_id: int = payload.get("id")
        if player_id is None:
            raise exception()
        exp: datetime = datetime.utcfromtimestamp(payload.get("exp"))
        if datetime.utcnow() >= exp:
            raise exception("Token expired")
    except JWTError:
        raise exception()
    player = crud.get_player(db, player_id)
    if not player:
        raise exception()
    return player


def get_lobby(player: Player = Depends(get_player)) -> Lobby:
    lobby = player.lobby
    if lobby is not None:
        return lobby
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "Player is not in a lobby")


def success(msg: str = "Success"):
    return Response(msg)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/login/{name}", response_model=Token)
async def login(name: str, db: Session = Depends(get_db)):
    access_token = create_access_token(db, name)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/logout")
async def logout(db: Session = Depends(get_db), player: Player = Depends(get_player)):
    crud.delete_player(db, player)
    return success()


async def leave_lobby(db: Session, player: Player):
    lobby = get_lobby(player)
    # first player is always host
    if player == lobby.host and len(lobby.player) == 1:
        crud.delete_lobby(db, lobby)
    else:
        lobby.player.remove(player)


@app.get("/create")
async def create_lobby(db: Session = Depends(get_db), player: Player = Depends(get_player)):
    if player.lobby is not None:
        await leave_lobby(db, player)
    lobby = crud.create_lobby(db, player)
    return {"code": lobby.code, "id": player.id}


@app.get("/join/{lobby_code}")
async def join_lobby(lobby_code: str, db: Session = Depends(get_db), player: Player = Depends(get_player)):
    lobby = crud.get_lobby_by_code(db, lobby_code)
    if lobby is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Can't find lobby")
    lobby.player.append(player)
    return {"id": player.id}


@app.get("/kick/{player_id}")
async def kick_player(player_id: int, player: Player = Depends(get_player), lobby: Lobby = Depends(get_lobby)):
    if player != lobby.host:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only host can kick players")
    for p in lobby.player:
        if p.id == player_id:
            player = p
            break
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Can't find player in lobby")
    lobby.player.remove(player)
    return success()


@app.get("/leave")
async def leave(db: Session = Depends(get_db), player: Player = Depends(get_player)):
    await leave_lobby(db, player)
    return success()


@app.get("/start")
async def start_game(lobby: Lobby = Depends(get_lobby)):
    lobby.started = True
    return success()


@app.get("/finish")
async def finish_game(db: Session = Depends(get_db), lobby: Lobby = Depends(get_lobby)):
    crud.delete_lobby(db, lobby)
    return success()


@app.post("/pos")
async def upload_position(pos: PositionUpdate, player: Player = Depends(get_player)):
    player.pos = pos.coordinates
    return success()


@app.get("/player", response_model=list[PlayerBase])
async def get_player_positions(lobby: Lobby = Depends(get_lobby)):
    return [p.__dict__ for p in lobby.player]
