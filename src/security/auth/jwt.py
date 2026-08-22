import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt

from fastapi import Depends, Response
from fastapi.security import OAuth2PasswordBearer

from models.user import User
from repository.legacy.user import get_user_by_username

# Module for creating JWT token

OAUTH2_SCHEME = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="login"))]

# JWT Config #
# openssl rand -hex 32
SECRET_KEY = "7f96f62d5f86f3a43dbe170f9d61e3262a65fe62f0db77d812b4dbfea2acc9be"
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRATION_MINS = 120

# steps 3-5: build a signature (crypto), glue user data + signature, and produce the final token,
# all in one call via jwt.encode -- a real crypto function replaces the mock signature+glue split
def create_access_token(
    data: dict,
    expires_delta: timedelta | None = timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINS),
) -> str:
    to_encode = data.copy()
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
def decode_token(token: str) -> str | None:
    try:
        # let a real decoding and verification algo handle it, unlike in legacy auth
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # username
        return payload.get("sub")  
    except jwt.InvalidTokenError:
        return None


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
async def auth_and_get_current_user(token: OAUTH2_SCHEME) -> User | None:
    username = decode_token(token)
    if username is None:
        return None

    return get_user_by_username(username)


AUTH_AND_GET_CURRENT_USER = Annotated[User | None, Depends(auth_and_get_current_user)]