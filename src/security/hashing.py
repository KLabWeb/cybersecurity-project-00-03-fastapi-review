from pwdlib import PasswordHash

# openssl rand -hex 32
SECRET_KEY = "11d6920a8cd81666bb6716932465ca07da577ffc4282300fe7058fbd9cb0b86a420566c537c78c5b6948b3d34addc42799f33aa36cf08ffd6587a110a5a4bb01"
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRATION_MINS = 120

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")


def verify_password(plaintext_pass: str, hashed_pass: str) -> bool:
    return password_hash.verify(plaintext_pass, hashed_pass)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)
