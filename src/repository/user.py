from random import randint

from pydantic import HttpUrl

from models.exception import DangerousUserIDException
from models.user import User
from security.hashing import get_password_hash


class UserRecord(User):
    hashed_password: str


# Obviously never store plaintext passwords like this in a real application
test_users: list[UserRecord] = [
    UserRecord(id=0, username="sleepycat24", hashed_password=get_password_hash("8&19djd81d8a219@"), image=None),
    UserRecord(
        id=1, username="grimANDfrostbitten", hashed_password=get_password_hash("thepassword1827$7G!"), image=None
    ),
    UserRecord(
        id=2,
        username="test-user",
        hashed_password=get_password_hash("passphrasewalrusleaflitterbirds"),
        image=HttpUrl("http://www.google.com"),
    ),
]


def get_user_by_id(user_id: int) -> User | None:
    # Mock a repo level exception occuring only some of the time
    dangerous_number = randint(0, 10)
    if user_id == dangerous_number:
        raise DangerousUserIDException(user_id=user_id)

    for test_user in test_users:
        if test_user.id == user_id:
            return test_user


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
            