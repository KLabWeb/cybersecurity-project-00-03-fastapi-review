from pydantic import BaseModel

from models.user import User
from security.auth import ADMIN, STAFF


class PasswordVerificationUserRequest(User):
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 2,
                    "username": "TomDickAndHarry",
                    "image": "http://www.tom-site.com",
                    "password": "badpassword",
                }
            ]
        }
    }


class LoginFormRequest(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}


class UserRoleVerificationResponse(BaseModel):
    user_id: int
    is_staff: bool
    is_admin: bool

class LoginFormResponse(BaseModel):
    username: str
