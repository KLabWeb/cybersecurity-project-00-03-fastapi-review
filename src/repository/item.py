from datetime import date

from models.item import Color, Item

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
