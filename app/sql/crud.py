from datetime import datetime

from config import LOBBY_EXPIRE, PLAYER_EXPIRE
from sql import models
from sqlalchemy.orm import Session

import schemas


def get_player(db: Session, player_id: int) -> schemas.Player:
    first = db.query(models.Player).filter(models.Player.id == player_id)
    first.update({models.Player.last_access: datetime.utcnow()})
    db.commit()
    return first.first()


def get_lobby_by_code(db: Session, code: str) -> schemas.Lobby:
    return db.query(models.Lobby).filter(models.Lobby.code == code).first()


def update_player_pos(db: Session, player_id: int, pos: str):
    db.query(models.Player).filter(models.Player.id == player_id).update({models.Player.pos: pos})
    db.commit()


def create_player(db: Session, name: str) -> schemas.Player:
    db_player = models.Player(name=name, last_access=datetime.utcnow())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def create_lobby(db: Session, player: models.Player) -> schemas.Lobby:
    code = format(hash(player.id), '02X')
    db_lobby = models.Lobby(code=code, created_at=datetime.utcnow(), player=[player])
    db.add(db_lobby)
    db.commit()
    db.refresh(db_lobby)
    return db_lobby


def delete_player(db: Session, player: models.Player):
    db.delete(player)
    db.commit()


def delete_lobby(db: Session, lobby: models.Lobby):
    db.delete(lobby)
    db.commit()


def delete_old_lobbies(db: Session) -> int:
    return db.query(models.Lobby).filter(models.Lobby.created_at + LOBBY_EXPIRE >= datetime.utcnow()).delete()


def delete_old_player(db: Session) -> int:
    return db.query(models.Player).filter(models.Player.last_access + PLAYER_EXPIRE >= datetime.utcnow()).delete()
