from datetime import datetime
from typing import Optional, Union

from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship, Mapped

from sql.database import Base


# CREATE TABLE lobbies (
# 	id INTEGER NOT NULL,
# 	code VARCHAR,
# 	created_at TIMESTAMP,
# 	started BOOLEAN,
# 	PRIMARY KEY (id)
# )
# CREATE UNIQUE INDEX ix_player_id ON player (id)
class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    name: Mapped[str] = Column(String)
    mister_x: Mapped[bool] = Column(Boolean, default=False)
    pos: Mapped[Union[str, None]] = Column(String)

    created_at: Mapped[datetime] = Column(TIMESTAMP)
    lobby_id: Mapped[Union[int, None]] = Column(ForeignKey("lobbies.id"))
    lobby: Mapped[Optional["Lobby"]] = relationship("Lobby", back_populates="player")


# CREATE TABLE player (
# 	id INTEGER NOT NULL,
# 	name VARCHAR,
# 	mister_x BOOLEAN,
# 	pos VARCHAR,
# 	created_at TIMESTAMP,
# 	lobby_id INTEGER,
# 	PRIMARY KEY (id),
# 	FOREIGN KEY(lobby_id) REFERENCES lobbies (id)
# )
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
