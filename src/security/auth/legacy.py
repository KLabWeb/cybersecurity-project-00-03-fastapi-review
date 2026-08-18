from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from models.user import User
from repository.legacy.user import get_user_by_username

# Module for building and verifying user authentication details
# via mock token system

OAUTH2_SCHEME = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]

MOCK_SECRET_KEY = "mock-secret"
TOKEN_EXPIRE = datetime.now() + timedelta(days=2)


# Build a signature by feeding a user data string (username + expiration)
# and the server-side secret auth key into a crypto function.
# Obvisouly this is terrible crypto & not prod ready
def build_signature(
    username: str, secret: str = MOCK_SECRET_KEY, expire: datetime = TOKEN_EXPIRE
) -> str:
    return f"{username}{expire.strftime('%Y%m%d%H%M%S')}{secret}"


# Glue the user data string and signature together with a period -- the final token
def build_token(username: str) -> str:
    return f"{username}.{build_signature(username)}"


# take in token and split out username from it
# verify signature matches for username
# return username as long as sig matches
def verify_and_decode_token(token: str) -> str | None:
    try:
        username, signature = token.split(".")
    except ValueError:
        return None

    if build_signature(username) != signature:
        return None

    return username


# verify token signature and get username from token
# then use username to get and return user
async def auth_and_get_current_user(
    token: OAUTH2_SCHEME,
) -> User | None:
    username = verify_and_decode_token(token)
    if username is None:
        return None

    return get_user_by_username(username)


AUTH_AND_GET_CURRENT_USER = Annotated[User | None, Depends(auth_and_get_current_user)]
