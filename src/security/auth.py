from repository.user import get_user_by_id
from security.hashing import DUMMY_HASH, verify_password


# if no user verify pass against DUMMY_HASH
# this ensures server has about same response time regardless of if user of no user
# to prevent attacker timining probing for user vs no user on server
def authenticate_user(user_id: int, password: str) -> bool:
    user = get_user_by_id(user_id)

    if not user:
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return True
