from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")


def verify_password(plaintext_pass: str, hashed_pass: str) -> bool:
    return password_hash.verify(plaintext_pass, hashed_pass)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)
