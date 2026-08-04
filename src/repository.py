from fastapi import HTTPException
from pydantic import BaseModel, HttpUrl
from models.item import Color, Item
from models.exception import DangerousUserIDException
from models.user import User
from models.purchase import Purchase
from datetime import date
from pwdlib import PasswordHash
from random import randint

class UserRecord(User):
    hashed_password: str

# openssl rand -hex 32
SECRET_KEY="11d6920a8cd81666bb6716932465ca07da577ffc4282300fe7058fbd9cb0b86a420566c537c78c5b6948b3d34addc42799f33aa36cf08ffd6587a110a5a4bb01"
ALGORITHM="HS512"
ACCESS_TOKEN_EXPIRATION_MINS = 120

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

def verify_password(plaintext_pass: str, hashed_pass: str) -> bool:
    return password_hash.verify(plaintext_pass, hashed_pass)

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

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
        

test_items: list[Item] = [
    Item(
        id=0,
        name="Apple",
        price=0.41,
        is_offer=True,
        created_on=date(2026, 3, 1),
        updated_on=date(2026, 4, 15),
    ),
    Item(
        id=1,
        name="Pear",
        price=0.49,
        is_offer=False,
        created_on=date(2026, 4, 12),
        updated_on=date(2026, 5, 25),
    ),
    Item(
        id=2,
        name="Pineapple",
        price=2.49,
        is_offer=False,
        created_on=date(2026, 1, 27),
        updated_on=date(2026, 3, 19),
    ),
    Item(
        id=3,
        name="Peach",
        price=0.57,
        is_offer=False,
        created_on=date(2026, 2, 18),
        updated_on=date(2026, 6, 29),
    ),
    Item(
        id=4,
        name="Plum",
        price=0.49,
        is_offer=False,
        created_on=date(2026, 1, 17),
        updated_on=date(2026, 5, 22),
    ),
]


def get_item_by_id(item_id: int) -> Item | None:
    for test_item in test_items:
        if test_item.id == item_id:
            return test_item
        
    return None


def get_item_index_by_item_id(item_id: int) -> int | None:
    for index, test_item in enumerate(test_items):
        if test_item.id == item_id:
            return index
        
    return None


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

test_purchases: list[Purchase] = [
    Purchase(id=0, user_id=0, item_id=0),
    Purchase(id=1, user_id=1, item_id=0),
    Purchase(id=2, user_id=0, item_id=1),
    Purchase(id=3, user_id=3, item_id=3),
    Purchase(id=4, user_id=1, item_id=2),
    Purchase(id=5, user_id=0, item_id=1),
    Purchase(id=6, user_id=0, item_id=0),
]


def get_items_below_price(max_price: float) -> list[Item]:
    return list(filter(lambda item: item.price < max_price, test_items))


def get_items_by_id_range(start: int, exclusive_end: int) -> list[Item]:
    return test_items[start:exclusive_end]


def put_item(item: Item) -> Item:
    test_items.append(item)
    return item


def replace_item(item_id: int, item: Item) -> Item | None:
    existing_item_index = get_item_index_by_item_id(item_id)

    if existing_item_index is None:
        return None

    test_items[existing_item_index] = item
    
    return test_items[existing_item_index]

def set_offer_if_expensive(item_id: int, item: Item, expensive_price: float) -> Item | None:
    existing_item = get_item_by_id(item_id)
    
    if not existing_item:
        return None

    if existing_item.price > expensive_price:
        existing_item.is_offer = item.is_offer
        existing_item.price = item.price

    return existing_item


def update_item_color(item_id: int, color: Color) -> Item | None:
    existing_item = get_item_by_id(item_id)

    if not existing_item:
        return None

    existing_item.color = color

    return existing_item


def get_user_by_id(user_id: int) -> UserRecord | None:
    # Mock a repo level exception occuring only some of the time
    dangerous_number = randint(0, 10)
    if user_id == dangerous_number:
        raise DangerousUserIDException(user_id=user_id)
    
    for test_user in test_users:
        if test_user.id == user_id:
            return test_user


def get_user_by_username(username: str) -> UserRecord | None:
    for test_user in test_users:
        if test_user.username == username:
            return test_user


def get_purchases() -> list[Purchase]:
    return test_purchases


def get_purchases_by_user_id(user_id: int) -> list[Purchase]:
    return [purchase for purchase in test_purchases if purchase.user_id == user_id]


def put_purchase_from_item_and_user(
    user: User, item: Item, manager_discount: bool
) -> Purchase:
    purchase_id = test_purchases[-1].id + 1
    purchase = Purchase(
        id=purchase_id,
        user_id=user.id,
        item_id=item.id,
        manager_discount=manager_discount,
    )

    test_purchases.append(purchase)
    return purchase
