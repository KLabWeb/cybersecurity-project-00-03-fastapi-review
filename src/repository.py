from fastapi import HTTPException
from models.item import Item
from models.user import User
from models.purchase import Purchase
from datetime import date

test_items: list[Item] = [
    Item(id=0, name="Apple", price=0.41, is_offer=True, created_on=date(2026, 3, 1), updated_on=date(2026, 4, 15)),
    Item(id=1, name="Pear", price=0.49, is_offer=False, created_on=date(2026, 4, 12), updated_on=date(2026, 5, 25)),
    Item(id=2, name="Pineapple", price=2.49, is_offer=False, created_on=date(2026, 1, 27), updated_on=date(2026, 3, 19)),
    Item(id=3, name="Peach", price=0.57, is_offer=False, created_on=date(2026, 2, 18), updated_on=date(2026, 6, 29)),
    Item(id=4, name="Plum", price=0.49, is_offer=False, created_on=date(2026, 1, 17), updated_on=date(2026, 5, 22)),
]

def get_item_by_id(item_id: int) -> Item:
    for test_item in test_items:
        if test_item.id == item_id:
            return test_item

    # this should not be raised here as doing so violates DDD
    # define custom HTTPException in Item model once get to FastAPI exception handling
    raise HTTPException(status_code=404, detail="Item not found")#

test_users: list[User] = [
    User(id=0, username="sleepycat24"),
    User(id=1, username="grimANDfrostbitten"),
    User(id=2, username="test-user"),
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

def get_items() -> list[Item]:
    return test_items

def get_items_by_id_range(start: int, exclusive_end: int) -> list[Item]:
    return test_items[start:exclusive_end]

def put_item(item: Item) -> Item:
    test_items.append(item)
    return item

def get_user_by_id(user_id: int) -> User:
    for test_user in test_users:
        if test_user.id == user_id:
            return test_user

    # this should not be raised here as doing so violates DDD
    # define custom HTTPException in Item model once get to FastAPI exception handling
    raise HTTPException(status_code=404, detail="User not found")#

def get_purchases() -> list[Purchase]:
    return test_purchases

def get_purchases_by_user_id(user_id: int) -> list[Purchase]:
    return [purchase for purchase in test_purchases if purchase.user_id == user_id]

def put_purchase_from_item_and_user(user: User, item: Item, manager_discount: bool) -> Purchase:
    purchase_id = test_purchases[-1].id + 1
    purchase = Purchase(id=purchase_id, user_id=user.id, item_id=item.id, manager_discount=manager_discount)
    
    test_purchases.append(purchase)
    return purchase