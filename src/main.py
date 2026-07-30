from fastapi import FastAPI, Query
from typing import Annotated

from api.requests import (
    GetItemsQueryFilter,
    GetItemQueryFilter,
    GetTwoItemsQueryFilter,
)

from api.responses import (
    ItemQueryResponse, 
    ItemUpdateResponse, 
    GetPurchasesResponse
)

from models.item import Item, Color, ItemID
from models.purchase import Purchase
from models.user import User

from repository import (
    test_items, 
    get_item_by_id, 
    get_purchases_by_user_id, 
    get_user_by_id
)

app = FastAPI()


# Most basic GET path to get root of API
@app.get("/")
async def get_root() -> dict[str, str]:
    return {"Hello": "World"}


# Path which returns all items
@app.get("/items")
async def get_items(
    filter_query: Annotated[GetItemsQueryFilter, Query()],
) -> list[Item]:
    return test_items


# Path takes path parameter to ID resource and get specific item
# ItemID carries the bounds validation, see models/item.py
# Regex Query validator checks if query has a least one letter
@app.get("/items/{item_id}")
async def get_item(
    item_id: ItemID,
    q: Annotated[GetItemQueryFilter, Query()],
) -> ItemQueryResponse:
    existing_item = get_item_by_id(item_id)
    return ItemQueryResponse(item_id=existing_item.id, query=q.q if q.q else None)


# Path which creates item via request body details
@app.post("/items")
async def create_item(item: Item) -> Item:
    test_items.append(item)
    return item


# Path which updates whole Item via request body details
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> ItemUpdateResponse:
    existing_item = get_item_by_id(item_id)

    existing_item.name = item.name
    existing_item.price = item.price
    existing_item.color = item.color
    existing_item.is_offer = item.is_offer

    return ItemUpdateResponse(
        item_id=existing_item.id,
        item_name=existing_item.name,
        color=existing_item.color,
        is_offer=existing_item.is_offer,
    )


# Path which only allows setting specific color names for updating color only
@app.patch("/items/{item_id}/color")
async def update_item_color(item_id: int, color: Color) -> Item:
    existing_item = get_item_by_id(item_id)
    existing_item.color = color

    return existing_item


# Path which uses a query param to filter items chepaer than max_price
@app.get("/items/")
async def get_cheap_items(max_price: float) -> list[Item]:
    return list(filter(lambda item: item.price < max_price, test_items))


# Path which uses path param, query param, and request body
# Path param gets item, query param filters item, request body gives update data
# Really don't need to pass in whole item here, but works for tutorial purposes
@app.patch("/items/{item_id}")
async def set_offer_if_item_expensive(
    item_id: int, item: Item, expensive_price: float
) -> Item:
    existing_item = get_item_by_id(item_id)

    if existing_item.price > expensive_price:
        existing_item.is_offer = item.is_offer
        existing_item.price = item.price

    return existing_item


# Path which gets two items using query param of list type via Query validation
# Obvisouly never define an endpoint like this (to just get two items) in a real system
@app.get("/two_items/")
async def get_two_items(
    id: Annotated[GetTwoItemsQueryFilter, Query()],
) -> list[Item]:
    return[get_item_by_id(id.id[0]), get_item_by_id(id.id[1])]


@app.get("/purchases/{user_id}")
async def get_purchases(user_id: int) -> GetPurchasesResponse:
    purchases = get_purchases_by_user_id(user_id=user_id)

    user = get_user_by_id(user_id=user_id)
    items_purchased = [get_item_by_id(purchase.item_id) for purchase in purchases]

    return GetPurchasesResponse(
        user=user, 
        items_purchased=items_purchased
    )

@app.put("/purchases/{purchase_id}")
async def create_purchase(user: User, item: Item):
    pass