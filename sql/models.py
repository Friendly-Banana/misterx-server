from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped

from database import Base


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    pos: Mapped[str | None] = Column()

    lobby_id: Mapped[int | None] = Column(ForeignKey("lobbies.id"))
    lobby: Mapped[Optional["Lobby"]] = relationship(back_populates="player")


class Lobby(Base):
    __tablename__ = "lobbies"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    created = Column(TIMESTAMP)
    host = Column(Player, ForeignKey("player.id"))
    started = Column(bool)

    player: Mapped[list["Player"]] = relationship(back_populates="player")
