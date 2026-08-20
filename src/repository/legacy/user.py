from enum import Enum
from random import randint

from data.legacy.user import raw_users
from models.exception import DangerousUserIDException
from models.user import User
from security.hashing import get_password_hash


class UserRole(Enum):
    STAFF = "staff"
    ADMIN = "admin"


class UserRecord(User):
    role: UserRole
    hashed_password: str


test_users: list[UserRecord] = [
    UserRecord(**raw_user, hashed_password=get_password_hash(raw_user["password"]))
    for raw_user in raw_users
]


def get_user_record_by_id(user_id: int) -> UserRecord | None:
    for test_user in test_users:
        if test_user.id == user_id:
            return test_user
        
def get_user_record_by_username(username: str) -> UserRecord | None:
    for test_user in test_users:
        if test_user.username == username:
            return test_user


def get_user_auth_by_username(username: str) -> str | None:
    test_user = get_user_record_by_username(username)

    return test_user.hashed_password if test_user else None


def get_user_roles_by_id(user_id: int) -> UserRole | None:
    test_user = get_user_record_by_id(user_id)

    return test_user.role if test_user else None


def get_user_by_id(user_id: int) -> User | None:
    # Mock a repo level exception occuring only some of the time
    dangerous_number = randint(0, 10)
    if user_id == dangerous_number:
        raise DangerousUserIDException(user_id=user_id)

    for test_user in test_users:
        if test_user.id == user_id:
            return test_user

    return None


def get_user_by_username(username: str) -> User | None:
    for test_user in test_users:
        if test_user.username == username:
            return test_user


# Uses exclude_unset to remove default val for User set during creation time during update
def patch_updated_user(user_id: int, user: User) -> User | None:
    for index, test_user in enumerate(test_users):
        if test_user.id == user_id:
            no_default_val_user = user.model_dump(exclude_unset=True, exclude={"id"})
            updated_existing_user = test_user.model_copy(update=no_default_val_user)
            test_users[index] = updated_existing_user

            return updated_existing_user
