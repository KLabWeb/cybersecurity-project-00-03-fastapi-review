from models.item import Item
from models.purchase import Purchase
from models.user import User

test_purchases: list[Purchase] = [
    Purchase(id=0, user_id=0, item_id=0),
    Purchase(id=1, user_id=1, item_id=0),
    Purchase(id=2, user_id=0, item_id=1),
    Purchase(id=3, user_id=3, item_id=3),
    Purchase(id=4, user_id=1, item_id=2),
    Purchase(id=5, user_id=0, item_id=1),
    Purchase(id=6, user_id=0, item_id=0),
]


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
