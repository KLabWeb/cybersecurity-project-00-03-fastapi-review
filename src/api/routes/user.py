from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Path, Request, Response
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import app
from api.models.users import (
    LoginFormRequest,
    LoginFormResponse,
    PasswordVerificationUserRequest,
    UserRoleVerificationResponse,
)
from models.exception import DangerousUserIDException
from models.item import UserID
from models.user import User, Token
from repository.legacy.user import (
    get_user_by_id as repo_get_user_by_id,
    get_user_by_username as repo_get_user_by_username,
    get_user_record_by_username,
    patch_updated_user,
)
from security.auth.verify import authenticate_user, ADMIN, STAFF
from security.auth.legacy import AUTH_AND_GET_CURRENT_USER as LEGACY_AUTH
from security.auth.jwt import JWT_AUTH_ADMIN
from security.auth.jwt import JWT_AUTH_STAFF
from security.auth.jwt import (
    create_access_token,
    get_allowed_scopes,
    set_token_cookie,
    TokenData,
)

router = APIRouter(
    tags=["users"],
)

# First endpoint
@router.get("/users/{user_id}")
async def get_user_by_id(user_id: Annotated[UserID, Path()]) -> User:
    existing_item = repo_get_user_by_id(user_id)

    if existing_item is None:
        raise HTTPException(status_code=404, detail="User not found")

    return existing_item


# Uses legacy auth flow AUTH_AND_GET_CURRENT_USER
# Auth verifies token, then gets user
@router.get("/users/username/{username}")
async def get_user_by_username(username: str, current_user: LEGACY_AUTH) -> User:
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate user credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    existing_item = repo_get_user_by_username(username)

    if existing_item is None:
        raise HTTPException(status_code=404, detail="User not found")

    return existing_item


# Uses JWT auth flow AUTH_AND_GET_CURRENT_USER
# Auth verifies token, then patches the user found by username
@router.patch("/users/username/{username}")
async def update_user_by_username(
    username: str, user: User, current_user: JWT_AUTH_ADMIN
) -> User:

    existing_user = repo_get_user_by_username(username)

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = patch_updated_user(user_id=existing_user.id, user=user)

    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.patch("/users/current")
async def update_current_user(user: User, current_user: JWT_AUTH_STAFF) -> User:
    updated_user = patch_updated_user(user_id=current_user.id, user=user)

    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
) -> Token:
    user_record = get_user_record_by_username(form_data.username)
    if user_record is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not authenticate_user(user_record.username, form_data.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    scopes = get_allowed_scopes(
        allowed_scopes=user_record.scopes, requested_scopes=form_data.scopes
    )

    token_data = TokenData(sub=user_record.username, scopes=scopes)

    access_token = create_access_token(token_data=token_data)

    set_token_cookie(access_token=access_token, response=response)

    return Token(access_token=access_token, token_type="bearer")


# Path which reads in a Form and stores in memory
@router.post("/form-login")
async def login_via_form(
    form_data: Annotated[LoginFormRequest, Form()],
) -> LoginFormResponse:
    user_record = repo_get_user_by_username(form_data.username)

    if user_record is None or not authenticate_user(
        user_record.username, form_data.password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return LoginFormResponse(username=form_data.username)


# Path which patches user via selective updating of model props
@router.patch("/users/{user_id}")
async def update_user(user_id: Annotated[UserID, Path()], user: User) -> User:
    updated_user = patch_updated_user(user_id=user_id, user=user)

    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


# Do not return a bool for auth like this but a Token, instead
# Not up to auth section in docs yet, so this works as a placeholder to demonstrate model inheritance section of docs
@router.post("/users/auth/verify")
async def verify_user_password(user: PasswordVerificationUserRequest) -> bool:
    if not authenticate_user(user.username, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return True


# Endpoint which uses a class instance as a dependency
@router.get("/users/{user_id}/roles")
async def verify_user_roles(
    user_id: Annotated[UserID, Path()],
    is_staff: Annotated[bool, Depends(STAFF)],
    is_admin: Annotated[bool, Depends(ADMIN)],
) -> UserRoleVerificationResponse:

    return UserRoleVerificationResponse(
        user_id=user_id, is_staff=is_staff, is_admin=is_admin
    )


# Custom exception handler for when getting an item but item is too dangerous
# DangerousUserIDException overrides RequestValidationError and it's @app exception handler
# Example: can occur in repository for get_item_by_id()
@app.exception_handler(DangerousUserIDException)
async def dangerous_id_exception_handler(
    request: Request, exc: DangerousUserIDException
):
    message = "Validation errors:"
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"
    return PlainTextResponse(message, status_code=418)
