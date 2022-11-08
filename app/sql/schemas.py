from datetime import datetime
from typing import Union

from pydantic import BaseModel


class PositionUpdate(BaseModel):
    # tuple[float, float] not suitable for db
    coordinates: str


class PlayerBase(BaseModel):
    id: int
    name: str
    mister_x: bool
    pos: Union[str, None]


class Player(PlayerBase):
    last_access: datetime
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
