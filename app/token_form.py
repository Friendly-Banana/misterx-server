from fastapi.exceptions import HTTPException
from fastapi.security.base import SecurityBase
from pydantic import Field
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class TokenBearer(SecurityBase):
    type_ = Field("bearer", alias="type")
    tokenUrl: str

    def __init__(self, token_url: str):
        self.tokenUrl = token_url


class TokenGetter(SecurityBase):
    def __init__(self, token_url: str = "/token"):
        self.model = TokenBearer(token_url=token_url)
        self.scheme_name = "bearer"

    async def __call__(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")
        if authorization is not None:
            scheme, _, token = authorization.partition(" ")
            if scheme.lower() == self.scheme_name:
                return token
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
        )
