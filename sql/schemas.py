import datetime

from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    lobby_id: int
    pos: str

    class Config:
        orm_mode = True


class LobbyBase(BaseModel):
    email: str


class LobbyCreate(LobbyBase):
    pass


class Lobby(LobbyBase):
    id: int
    created: datetime.datetime
    started: bool
    host: Player
    player: list[Player] = []

    class Config:
        orm_mode = True
