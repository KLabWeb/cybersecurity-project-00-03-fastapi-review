from fastapi import HTTPException
from models.item import Item
from datetime import date

test_items: list[Item] = [
    Item(id=0, name="Apple", price=0.41, is_offer=True, created_on=date(2026, 3, 1), updated_on=date(2026, 4, 15), tags=["fiber dense", "worm"]),
    Item(id=1, name="Pear", price=0.49, is_offer=False, created_on=date(2026, 4, 12), updated_on=date(2026, 5, 25)),
    Item(id=2, name="Pineapple", price=2.49, is_offer=False, created_on=date(2026, 1, 27), updated_on=date(2026, 3, 19)),
    Item(id=3, name="Peach", price=0.57, is_offer=False, created_on=date(2026, 2, 18), updated_on=date(2026, 6, 29)),
]


def get_item_by_id(item_id: int) -> Item:
    for test_item in test_items:
        if test_item.id == item_id:
            return test_item

    # this should not be raised here as doing so violates DDD
    # define custom HTTPException in Item model once get to FastAPI exception handling
    raise HTTPException(status_code=404, detail="Item not found")#
