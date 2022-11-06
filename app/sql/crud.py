from datetime import datetime

from sqlalchemy.orm import Session

from app.sql import models, schemas
from app.main import LOBBY_EXPIRE


def get_player(db: Session, player_id: int) -> schemas.Player:
    return db.query(models.Player).filter(models.Player.id == player_id).first()


def get_lobby_by_code(db: Session, code: str) -> schemas.Lobby:
    return db.query(models.Lobby).filter(models.Lobby.code == code).first()


def get_old_lobbies(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Lobby]:
    return db.query(models.Lobby).filter(models.Lobby.created_at + LOBBY_EXPIRE >= datetime.utcnow()).offset(
        skip).limit(limit).all()


def create_player(db: Session, name: str) -> schemas.Player:
    db_player = models.Player(verbose_name=name)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def create_lobby(db: Session, player: models.Player) -> schemas.Lobby:
    code = format(hash(player.id), '02X')
    db_lobby = models.Lobby(code=code, created=datetime.utcnow(), host=player, player=[player])
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
