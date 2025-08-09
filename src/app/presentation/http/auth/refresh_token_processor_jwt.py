import logging
from typing import Any, Literal, NewType, TypedDict, cast

import jwt

from app.domain.enums.user_role import UserRole

log = logging.getLogger(__name__)

JwtSecret = NewType("JwtSecret", str)
JwtAlgorithm = Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]


class RefreshPayload(TypedDict):
    sub: str
    email: str
    role: str
    exp: int


class JwtRefreshTokenProcessor:
    def __init__(self, secret: JwtSecret, algorithm: JwtAlgorithm):
        self._secret = secret
        self._algorithm = algorithm

    def encode(self, *, user_id: int, email: str, role: UserRole, exp_ts: int) -> str:
        payload = RefreshPayload(
            sub=str(user_id),
            email=email,
            role=role.value,
            exp=exp_ts,
        )
        return jwt.encode(cast(dict[str, Any], payload), key=self._secret, algorithm=self._algorithm)

    def decode(self, token: str) -> RefreshPayload:
        payload = jwt.decode(token, key=self._secret, algorithms=[self._algorithm])
        return cast(RefreshPayload, payload)


