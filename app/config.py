import os
from datetime import timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(hours=24)
LOBBY_EXPIRE = timedelta(hours=3)
PLAYER_EXPIRE = timedelta(days=1)
JWT_SIGNING_KEY = os.getenv('JWT_SIGNING_KEY')
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')
