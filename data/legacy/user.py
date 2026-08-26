# Raw user data for the legacy store
# Plain values only - the repository layer defines the model and builds from these
# Passwords are plaintext here as this API specifically meant to include security class violations, for later cybersecurity testing + fix work
# Obviously never store plaintext passwords like this in a real application
raw_users: list[dict] = [
    {
        "id": 0,
        "username": "sleepycat24",
        "password": "8&19djd81d8a219@",
        "scopes": ["read_all", "write_all", "read_self", "write_self"],
        "role": "admin",
        "image": None,
    },
    {
        "id": 1,
        "username": "grimANDfrostbitten",
        "password": "thepassword1827$7G!",
        "role": "staff",
        "scopes": ["read_self", "write_self"],
        "image": None,
    },
    {
        "id": 2,
        "username": "test-user",
        "password": "passphrasewalrusleaflitterbirds",
        "role": "staff",
        "scopes": ["read_self", "write_self"],
        "image": "http://www.google.com",
    },
]
