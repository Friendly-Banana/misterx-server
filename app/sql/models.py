from datetime import datetime
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped

from app.sql.database import Base


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    name: Mapped[str]
    misterX: Mapped[bool]
    pos: Mapped[str | None] = None

    lobby_id: Mapped[int | None] = Column(ForeignKey("lobbies.id"))
    lobby: Mapped[Optional["Lobby"]] = relationship("Lobby", back_populates="player")

    def to_json(self):
        return {"id": self.id, "name": self.name, "x": self.misterX, "pos": self.pos}


class Lobby(Base):
    __tablename__ = "lobbies"

    id = Column(Integer, primary_key=True)
    code: Mapped[str]
    created_at: Mapped[datetime]
    started: Mapped[bool]

    player: Mapped[list["Player"]] = relationship(Player, back_populates="lobby")

    @property
    def host(self):
        return self.player[0]
