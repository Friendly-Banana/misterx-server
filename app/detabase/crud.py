from datetime import datetime

from deta import Deta

import schemas
from config import LOBBY_EXPIRE, PLAYER_EXPIRE

deta = Deta()

player = deta.Base("player")
lobbies = deta.Base("lobbies")


def get_player(player_id) -> schemas.Player:
    return player.get(player_id)


def get_lobby_by_code(code: str) -> schemas.Lobby | None:
    lobbies_fetch = lobbies.fetch({"code": code}, 1)
    if lobbies_fetch.count == 0:
        return
    return lobbies_fetch.items[0]


def create_player(name: str) -> schemas.Player:
    db_player = models.Player(name=name, last_access=datetime.utcnow())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def create_lobby(player: models.Player) -> schemas.Lobby:
    code = format(hash(player.id), '02X')
    db_lobby = models.Lobby(code=code, created_at=datetime.utcnow(), player=[player])
    db.add(db_lobby)
    db.commit()
    db.refresh(db_lobby)
    return db_lobby


def delete_player(player: models.Player):
    db.delete(player)
    db.commit()


def delete_lobby(lobby: models.Lobby):
    db.delete(lobby)
    db.commit()


def delete_old_lobbies(skip: int = 0, limit: int = 100) -> int:
    return lobbies.filter(
        models.Lobby.last_access + LOBBY_EXPIRE >= datetime.utcnow()).offset(
        skip).limit(limit).delete()


def delete_old_player(skip: int = 0, limit: int = 100) -> int:
    return player.filter(
        models.Player.last_access + PLAYER_EXPIRE >= datetime.utcnow()).offset(
        skip).limit(limit).delete()
