from fastapi import Depends

from repository.user import get_user_auth_by_username, get_user_roles_by_id, UserRole
from security.hashing import DUMMY_HASH, verify_password

# Module for verifying user authentication details
# including username, password, and roles

# step 2: get user via login form username, hash form password, compare to stored hash to verify user
# if no user verify pass against DUMMY_HASH
# this ensures server has about same response time regardless of if user of no user
# to prevent attacker timining probing for user vs no user on server
def authenticate_user(username: str, password: str) -> bool:
    user_password = get_user_auth_by_username(username)

    if not user_password:
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, user_password):
        return False

    return True


# Class, which is used as a depency itself also Depends on repo function to get roles
class UserRoleVerifier:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user_role: UserRole = Depends(get_user_roles_by_id)) -> bool:
        return user_role in self.allowed_roles


# Role Config
STAFF = UserRoleVerifier(allowed_roles=[UserRole.STAFF])
ADMIN = UserRoleVerifier(allowed_roles=[UserRole.STAFF, UserRole.ADMIN])
