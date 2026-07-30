# main.py

from fastapi import FastAPI, Query
from typing import Annotated

from models import Item, Color
from data import test_items, get_item_by_id
from schemas import ItemQueryResponse, ItemUpdateResponse

app = FastAPI()
    
# Most basic GET path to get root of API
@app.get("/")
async def get_root() -> dict[str, str]:
    return {"Hello": "World"}

# Path which returns all items
@app.get("/items")
async def get_items() -> list[Item]:
    return test_items

# Path takes path parameter to ID resource and get specific item
# Regex checks if query has a least one letter
@app.get("/items/{item_id}")
async def get_item(item_id: int, q: Annotated[str | None, Query(min_length=31, max_length=50, pattern="[a-zA-Z]")] = None) -> ItemQueryResponse:
    existing_item = get_item_by_id(item_id)
    return ItemQueryResponse(item_id=existing_item.id, query=q if q else None)

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
async def set_offer_if_item_expensive(item_id: int, item: Item, expensive_price: float) -> Item:    
    existing_item = get_item_by_id(item_id)
    
    if existing_item.price > expensive_price:        
        existing_item.is_offer = item.is_offer
        existing_item.price = item.price
                
    return existing_item

# Path which gets two items using query param of list type
# Obvisouly never define an endpoint like this in a real system
@app.get("/two_items/")
async def get_two_items(q: Annotated[list[int], Query(min_length=2, max_length=2, title="Size restricter query", description="Ensure 2 and only 2 id are requested", alias="get-too")] = []) -> list[Item]:
    return [get_item_by_id(q[0]), get_item_by_id(q[1])]