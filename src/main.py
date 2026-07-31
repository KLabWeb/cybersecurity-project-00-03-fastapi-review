from fastapi import FastAPI, Body, Query, Path
from typing import Annotated

from api.requests import (
    GetItemsQueryFilter,
    GetItemQueryFilter,
    CompareItemsPricesQueryFilter,
)

from api.responses import (
    GetItemResponse,
    UpdateItemResponse,
    GetPurchasesResponse,
    ItemPriceInfo,
    CompareItemPricesResponse,
)

from models.item import Item, Color, ItemID
from models.purchase import Purchase
from models.user import User

from repository import (
    get_item_by_id,
    get_items_by_id_range,
    get_items as get_all_items,
    put_item,
    get_purchases as get_all_purchases,
    get_purchases_by_user_id,
    put_purchase_from_item_and_user,
    get_user_by_id,
)

app = FastAPI()


### root endpoint ###


# Most basic GET path to get root of API
@app.get("/")
async def get_root() -> dict[str, str]:
    return {"Hello": "World"}


### Item endpoints ###


# Path which returns all items
# Slices return based on offest and limit from Query request filter
@app.get("/items")
async def get_items(
    filter_query: Annotated[GetItemsQueryFilter, Query()],
) -> list[Item]:
    return get_items_by_id_range(
        filter_query.offset, (filter_query.limit + filter_query.offset)
    )


# Path which gets two items using query param of list type via Query validation
# Obvisouly never define an endpoint like this (to just get two items) in a real system
@app.get("/items/price-comparison")
async def compare_item_prices(
    id: Annotated[CompareItemsPricesQueryFilter, Query()],
) -> CompareItemPricesResponse:
    first_item = get_item_by_id(id.id[0])
    second_item = get_item_by_id(id.id[1])

    greater_price_item_id = (
        first_item.id
        if first_item.price > second_item.price
        else second_item.id if first_item.price < second_item.price else None
    )

    return CompareItemPricesResponse(
        item_price_info=[
            ItemPriceInfo(
                item_id=first_item.id,
                item_name=first_item.name,
                item_price=first_item.price,
            ),
            ItemPriceInfo(
                item_id=second_item.id,
                item_name=second_item.name,
                item_price=second_item.price,
            ),
        ],
        greater_price_item_id=greater_price_item_id,
    )

    return [get_item_by_id(id.id[0]), get_item_by_id(id.id[1])]


# Path takes path parameter to ID resource and get specific item
# ItemID carries the bounds validation via Path validation
# Regex Query validator checks if query has a least one letter
@app.get("/items/{item_id}")
async def get_item(
    item_id: Annotated[ItemID, Path()],
    q: Annotated[GetItemQueryFilter, Query()],
) -> GetItemResponse:
    existing_item = get_item_by_id(item_id)
    return GetItemResponse(
        item_id=existing_item.id, 
        item_name=existing_item.name, 
        query=q.q if q.q else None
    )


# Path which creates item via request body details
@app.post("/items")
async def create_item(item: Item) -> Item:
    return put_item(item)


# Path which updates whole Item via request body details
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> UpdateItemResponse:
    existing_item = get_item_by_id(item_id)

    existing_item.name = item.name
    existing_item.price = item.price
    existing_item.color = item.color
    existing_item.is_offer = item.is_offer

    return UpdateItemResponse(
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
    items = get_all_items()
    return list(filter(lambda item: item.price < max_price, items))


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


### Purchase endpoints ###

# Path which returns all purchases
@app.get("/purchases")
async def get_purchases() -> list[Purchase]:
    return get_all_purchases()


@app.get("/purchases/{user_id}")
async def get_purchases_by_user(user_id: int) -> GetPurchasesResponse:
    purchases = get_purchases_by_user_id(user_id=user_id)

    user = get_user_by_id(user_id=user_id)
    items_purchased = [get_item_by_id(purchase.item_id) for purchase in purchases]

    return GetPurchasesResponse(user=user, items_purchased=items_purchased)


# Path takes in two request bodies to create Purchase (an Item & User)
# Uses Body to pass in request body with only single primitive value
# Don't actually need two objects passed in here, as could just pass in IDs, but works for tutorial demo purposes
@app.put("/purchases")
async def create_purchase_from_item_and_user(user: User, item: Item, manager_discount: Annotated[bool, Body()]) -> Purchase:
    return put_purchase_from_item_and_user(user, item, manager_discount)
