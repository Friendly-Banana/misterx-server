from datetime import timedelta, datetime

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import engine, SessionLocal
from sql import models, schemas, crud

JWT_SIGNING_KEY = "9a1234d756b08fc143a5fd67c415c91d2c4bc4ddb2387c2aea1bc7eb35b632f7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(hours=24)
LOBBY_EXPIRE = timedelta(hours=3)

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Lobby:
    code: str | None
    player: list[int]


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict):
    # TODO create user in database
    to_encode = data.copy()
    expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRE
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SIGNING_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class Player(BaseModel):
    # TODO thread safe
    next_id = 0
    id: int
    username: str
    lobby: Lobby | None
    pos: str | None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = Player.next_id
        Player.next_id += 1


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SIGNING_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = Player(username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def success(msg: str = "Success"):
    return {"200": msg}


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = create_access_token(
        data={"sub": form_data.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/logout")
async def logout(db: Session = Depends(get_db)):
    return {"message": "Hello"}


@app.get("/create")
async def create(user: schemas.PlayerCreate, db: Session = Depends(get_db)):
    crud.create_player(db, user.name)
    return success()


@app.get("/join/{lobby_code}")
async def join(lobby_code: str, db: Session = Depends(get_db)):
    crud.create_player(db, user.name)
    return {"message": "Hello"}


@app.get("/kick/{player}")
async def kick(player: int, db: Session = Depends(get_db)):
    return {"message": "Hello"}


@app.get("/leave")
async def leave(, db: Session = Depends(get_db)):
    return {"message": "Hello"}


@app.get("/start")
async def start(, db: Session = Depends(get_db)):
    return {"message": "Hello"}


@app.get("/pos/{pos}")
async def upload_position(pos: str, db: Session = Depends(get_db)):
    return {"message": "Hello"}


@app.get("/player")
async def get_player_positions(, db: Session = Depends(get_db)):
    return {"message": "Hello"}
