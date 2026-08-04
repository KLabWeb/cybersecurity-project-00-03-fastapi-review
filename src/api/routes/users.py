from typing import Annotated

from fastapi import Form, HTTPException, Path, Request
from fastapi.responses import JSONResponse

from app import app
from api.models.users import LoginFormRequest, LoginFormResponse, PasswordVerificationUser
from models.exception import DangerousUserIDException
from models.item import UserID
from models.user import User
from repository.user import get_user_by_id, get_user_by_username
from security.auth import authenticate_user


@app.get("/users/{user_id}")
async def get_user(user_id: Annotated[UserID, Path()]) -> User:
    existing_item = get_user_by_id(user_id)

    if existing_item is None:
        raise HTTPException(status_code=404, detail="User not found")

    return existing_item


# Do not return a bool for auth like this but a Token, instead
# Not up to auth section in docs yet, so this works as a placeholder to demonstrate model inheritance section of docs
@app.post("/users/verify_auth")
async def verify_user_password(user: PasswordVerificationUser) -> bool:
    if not authenticate_user(user.id, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return True


# Path which reads in a Form and stores in memory
@app.post("/form_login")
async def login_via_form(form_data: Annotated[LoginFormRequest, Form()]) -> LoginFormResponse:
    user_record = get_user_by_username(form_data.username)

    if user_record is None or not authenticate_user(user_record.id, form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return LoginFormResponse(username=form_data.username)


# Custom exception handler for when getting an item but item is too dangerous
# Example: can occur in repository for get_item_by_id()
@app.exception_handler(DangerousUserIDException)
async def dangerous_id_exception_handler(request: Request, exc: DangerousUserIDException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Error: user id of '{exc.user_id}' for requested user is a dangerous id. Sorry, but we can't get this user."}
    )
