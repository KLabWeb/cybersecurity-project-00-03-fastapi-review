from datetime import datetime
from typing import Annotated
import json

from fastapi import Body, Cookie, Header, HTTPException, Path, Query, status
from fastapi.encoders import jsonable_encoder

from app import app
from api.models.items import (
    CompareItemPricesResponse,
    CompareItemsPricesQueryFilter,
    GetItemQueryFilter,
    GetItemResponse,
    GetItemsQueryFilter,
    ItemActionTags,
    ItemPriceInfoMetadata,
    UpdateItemResponse,
    ItemsJSONResponse,
)
from models.item import Color, Item, ItemID
from repository.item import (
    get_all_items,
    get_item_by_id,
    get_items_below_price,
    get_items_by_id_range,
    put_item,
    replace_item,
    set_offer_if_expensive,
    update_item_color as repo_update_item_color,
)


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
    current_datetime = datetime.now()

    first_item = get_item_by_id(id.id[0])
    second_item = get_item_by_id(id.id[1])

    if first_item is None or second_item is None:
        raise HTTPException(status_code=404, detail="One or both items not found")

    greater_price_item_id = (
        first_item.id
        if first_item.price > second_item.price
        else second_item.id if first_item.price < second_item.price else None
    )

    return CompareItemPricesResponse(
        item_price_info=[
            ItemPriceInfoMetadata(
                item_id=first_item.id,
                item_name=first_item.name,
                item_price=first_item.price,
                request_made=current_datetime,
            ),
            ItemPriceInfoMetadata(
                item_id=second_item.id,
                item_name=second_item.name,
                item_price=second_item.price,
                request_made=current_datetime,
            ),
        ],
        greater_price_item_id=greater_price_item_id,
    )


# Path takes path parameter to ID resource and get specific item
# ItemID carries the bounds validation via Path validation
# Regex Query validator checks if query has a least one letter
# Note how this endpoint also looks for a Cookie and Header being passed in w/ request
@app.get("/items/{item_id}")
async def get_item(
    item_id: Annotated[ItemID, Path()],
    q: Annotated[GetItemQueryFilter, Query()],
    last_item_id_viewed: Annotated[int | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
) -> GetItemResponse:
    existing_item = get_item_by_id(item_id)

    # Endpoint layer is in charge of HTTP communications in both responses & requests
    # As such, if an error occurs, like cannot find Item in repo, endpoint layer raises exception
    # And exception raised is in form that can be communicated via standard HTTP response
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return GetItemResponse(
        item_id=existing_item.id,
        item_name=existing_item.name,
        query=q.q if q.q else None,
    )


# Path which creates item via request body details
# Uses status to help fine proper status code to return
@app.post("/items", status_code=status.HTTP_201_CREATED, tags=[ItemActionTags.CREATE])
async def create_item(item: Item) -> Item:
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return put_item(item)


# Path which updates whole Item via request body details
# Also sets int to be embeded object inside request body
@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Annotated[Item, Body(embed=True)]
) -> UpdateItemResponse:
    updated_item = replace_item(item_id=item_id, item=item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return UpdateItemResponse(
        item_id=updated_item.id,
        item_name=updated_item.name,
        color=updated_item.color,
        is_offer=updated_item.is_offer,
    )


# Path which only allows setting specific color names for updating color only
@app.patch("/items/{item_id}/color")
async def update_item_color(item_id: int, color: Color) -> Item:
    updated_item = repo_update_item_color(item_id=item_id, color=color)

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated_item


# Path which uses a query param to filter items chepaer than max_price
@app.get("/items/")
async def get_cheap_items(max_price: float) -> list[Item]:
    return get_items_below_price(max_price=max_price)


# Path which uses path param, query param, and request body
# Path param gets item, query param filters item, request body gives update data
# Really don't need to pass in whole item here, but works for tutorial purposes
@app.patch("/items/{item_id}")
async def set_offer_if_item_expensive(
    item_id: int, item: Item, expensive_price: float, deprecated=True
) -> Item:
    updated_item = set_offer_if_expensive(item_id=item_id, item=item, expensive_price=expensive_price)

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated_item

# Uses FastAPI's jsonable_ecoder to get a json compatible obj (dict) from list[Item]
# Then converts dict of Items and converts it into json formatted string
@app.get("/items")
async def get_items_as_json() -> ItemsJSONResponse:
    items_list: list[Item] = get_all_items()
    
    if not items_list:
        raise HTTPException(status_code=404, detail="No items found")
    
    items_dict: dict = jsonable_encoder(items_list)
    items_str: str = json.dumps(items_dict)
    
    return ItemsJSONResponse(items=items_str)