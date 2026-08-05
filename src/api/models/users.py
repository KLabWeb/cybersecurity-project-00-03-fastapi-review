from pydantic import BaseModel

from models.user import User


class PasswordVerificationUser(User):
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


class LoginFormResponse(BaseModel):
    username: str
