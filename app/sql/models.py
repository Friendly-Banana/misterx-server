from datetime import datetime
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship, Mapped

from app.sql.database import Base


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    name: Mapped[str] = Column(String)
    mister_x: Mapped[bool] = Column(Boolean, default=False)
    pos: Mapped[str | None] = Column(String)

    created_at: Mapped[datetime] = Column(TIMESTAMP)
    lobby_id: Mapped[int | None] = Column(ForeignKey("lobbies.id"))
    lobby: Mapped[Optional["Lobby"]] = relationship("Lobby", back_populates="player")


class Lobby(Base):
    __tablename__ = "lobbies"

    id = Column(Integer, primary_key=True)
    code: Mapped[str] = Column(String)
    created_at: Mapped[datetime] = Column(TIMESTAMP)
    started: Mapped[bool] = Column(Boolean, default=False)

    player: Mapped[list["Player"]] = relationship(Player, back_populates="lobby")

    @property
    def host(self):
        return self.player[0]
