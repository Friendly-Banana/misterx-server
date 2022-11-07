from datetime import datetime

from pydantic import BaseModel


class PositionUpdate(BaseModel):
    # tuple[float, float] not suitable for db
    coordinates: str


class PlayerBase(BaseModel):
    id: int
    name: str
    mister_x: bool
    pos: str | None


class Player(PlayerBase):
    created_at: datetime
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
