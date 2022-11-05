from datetime import datetime

from sqlalchemy.orm import Session

import main
from . import models


def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()


def get_old_lobbies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lobby).filter(models.Lobby.created + main.LOBBY_EXPIRE >= datetime.utcnow()).offset(
        skip).limit(limit).all()


def create_player(db: Session, name: str):
    db_player = models.Player(name=name)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def create_lobby(db: Session, player: models.Player):
    db_lobby = models.Lobby(created=datetime.utcnow(), host=player)
    db.add(db_lobby)
    db.commit()
    db.refresh(db_lobby)
    return db_lobby


def delete_player(db: Session, player: models.Player):
    db.delete(player)
    db.commit()
