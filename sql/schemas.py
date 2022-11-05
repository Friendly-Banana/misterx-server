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
    host: Player


class LobbyCreate(LobbyBase):
    pass


class Lobby(LobbyBase):
    id: int
    code: str
    created: datetime.datetime
    started: bool
    player: list[Player] = []

    class Config:
        orm_mode = True
