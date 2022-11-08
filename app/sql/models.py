from datetime import datetime
from typing import Optional, Union

from sql.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship, Mapped


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    name: Mapped[str] = Column(String)
    mister_x: Mapped[bool] = Column(Boolean, default=False)
    pos: Mapped[Union[str, None]] = Column(String)

    last_access: Mapped[datetime] = Column(TIMESTAMP)
    lobby_id: Mapped[Union[int, None]] = Column(ForeignKey("lobbies.id"))
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
