from fastapi.exceptions import HTTPException, RequestValidationError


class DangerousUserIDException(RequestValidationError):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(
            [
                {
                    "loc": ("path", "user_id"),
                    "msg": f"User id of '{user_id}' for requested user is a dangerous id. Sorry, but we can't get this user.",
                }
            ]
        )


class PurchaseNotFoundException(Exception):
    def __init__(self, purchase_id: int):
        self.purchase_id = purchase_id


class CredentialsException(HTTPException):
    def __init__(self, authenticate_value: str):
        super().__init__(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )


class PermissionsException(HTTPException):
    def __init__(self, authenticate_value: str):
        super().__init__(
            status_code=403,
            detail="Invalid permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
