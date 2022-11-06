from datetime import datetime

from pydantic import BaseModel


class PlayerBase(BaseModel):
    id: int
    name: str
    misterX: bool
    pos: str


class Player(PlayerBase):
    lobby: "Lobby"

    class Config:
        orm_mode = True


class Lobby(BaseModel):
    id: int
    code: str
    created_at: datetime
    started: bool
    host: Player
    player: list[Player]

    class Config:
        orm_mode = True
