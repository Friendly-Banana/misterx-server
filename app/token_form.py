from fastapi.exceptions import HTTPException
from fastapi.security.base import SecurityBase
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class TokenGetter(SecurityBase):
    def __init__(self):
        self.scheme_name = "bearer"

    async def __call__(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")
        scheme, _, token = authorization.partition(" ")
        if not authorization or scheme.lower() != self.scheme_name:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        return token
