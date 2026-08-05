from fastapi.exceptions import RequestValidationError


class DangerousUserIDException(RequestValidationError):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(
            [{"loc": ("path," "user_id"), 
              "msg": f"User id of '{user_id}' for requested user is a dangerous id. Sorry, but we can't get this user."}]
        )