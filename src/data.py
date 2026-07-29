from models import Item

test_items: list[Item] = [
    Item(id=1, name="Apple", price=0.41, is_offer=True),
    Item(id=2, name="Pear", price=0.49, is_offer=False),
    Item(id=3, name="Pineapple", price=2.49, is_offer=False),
    Item(id=4, name="Peach", price=0.57, is_offer=False)
]