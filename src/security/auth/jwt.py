import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt

from fastapi import Depends, Response, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from pydantic import BaseModel

from models.exception import CredentialsException, PermissionsException
from models.user import User
from repository.legacy.user import get_user_by_username

# Module for creating JWT token
SCOPES = {
    "read_all": "read all data",
    "write_all": "write all data",
    "read_self": "only read data that belongs to current user",
    "write_self": "only write data that belongs to current user",
}

OAUTH2_SCHEME = Annotated[
    str, Depends(OAuth2PasswordBearer(tokenUrl="login", scopes=SCOPES))
]

# JWT Config #
# openssl rand -hex 32
SECRET_KEY = "7f96f62d5f86f3a43dbe170f9d61e3262a65fe62f0db77d812b4dbfea2acc9be"
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRATION_MINS = 120


class TokenData(BaseModel):
    sub: str | None
    scopes: list[str] = []


# steps 3-5: build a signature (crypto), glue user data + signature, and produce the final token,
# all in one call via jwt.encode -- a real crypto function replaces the mock signature+glue split
def create_access_token(
    token_data: TokenData,
    expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINS),
) -> str:
    to_encode = token_data.model_dump()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    # let a real encoding algo handle it, unlike in legacy auth
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# steps 7-8: split token via jwt.decode, which also reruns the crypto check on the signature,
# and return the user data (sub) if it matches -- one call replaces the mock split+recompute
def decode_token(token: str) -> dict | None:
    try:
        # let a real decoding and verification algo handle it, unlike in legacy auth
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return None


# Compare scopes user has requested as part of /login Token creation
# to scopes user is allowed to have. Return what they can have only.
def get_allowed_scopes(
    allowed_scopes: list[str], requested_scopes: list[str]
) -> list[str]:
    # if user does not request scopes, give them all their allowed scopes
    if not requested_scopes:
        return allowed_scopes

    return [scope for scope in requested_scopes if scope in allowed_scopes]


# append JWT token as cookie onto response
def set_token_cookie(access_token: str, response: Response) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=os.getenv("APP_ENV") == "production",
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRATION_MINS * 60,
    )


# verify token signature and get username from token
# then use username to get and return user
async def auth_and_get_current_user(
    token: OAUTH2_SCHEME, security_scopes: SecurityScopes
) -> User:
    # decode token & raise Exception with proper auth_value if cannot decode
    authenticate_value = (
        f'Bearer scope="{security_scopes.scope_str}"'
        if security_scopes.scopes
        else "Bearer"
    )

    payload = decode_token(token)

    if payload is None:
        raise CredentialsException(authenticate_value)

    # deconstruct payload into TokenData model
    token_data = TokenData(sub=payload.get("sub"), scopes=payload.get("scopes") or [])

    # validation 1. ensure sub exists on token
    if token_data.sub is None:
        raise CredentialsException(authenticate_value)

    # get user using sub &
    # validation 2. ensure user exists
    user = get_user_by_username(token_data.sub)

    if user is None:
        raise CredentialsException(authenticate_value)

    # validation 3. ensure user has required scopes for route
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise PermissionsException(authenticate_value)

    return user


JWT_AUTH_STAFF = Annotated[
    User, Security(auth_and_get_current_user, scopes=["read_self", "write_self"])
]

JWT_AUTH_ADMIN = Annotated[
    User, Security(auth_and_get_current_user, scopes=["read_all", "write_all"])
]
