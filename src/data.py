from fastapi import HTTPException
from models import Item

test_items: list[Item] = [
    Item(id=0, name="Apple", price=0.41, is_offer=True),
    Item(id=1, name="Pear", price=0.49, is_offer=False),
    Item(id=2, name="Pineapple", price=2.49, is_offer=False),
    Item(id=3, name="Peach", price=0.57, is_offer=False),
]


def get_item_by_id(item_id: int) -> Item:
    for test_item in test_items:
        if test_item.id == item_id:
            return test_item

    raise HTTPException(status_code=404, detail="Item not found")
