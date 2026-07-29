# main.py

from fastapi import FastAPI, HTTPException

from models import Item
from data import test_items
from models import Color

from schemas import ItemQueryResponse
from schemas import ItemUpdateResponse

app = FastAPI()
    
# Most basic GET path
@app.get("/")
async def read_root() -> dict:
    return {"Hello": "World"}

# Path which returns all items
@app.get("/items")
async def get_items() -> list[Item]:
    return test_items

# Path takes path parameter to ID resource
@app.get("/items/{item_id}")
async def get_item(item_id: int, q: str | None = None) -> ItemQueryResponse:
    return ItemQueryResponse(item_id=item_id, query=q)

# Path which creates item via request body details
@app.post("/items/{item_id}")
async def create_item(item: Item) -> Item:
    test_items.append(item)
    return item

# Path which updates whole Item via request body details
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> ItemUpdateResponse:
    return ItemUpdateResponse(item_id=item_id, item_name=item.name, is_offer=item.is_offer)

# Path which only allows getting specific color names
@app.get("/item-color/{color_id}")
async def get_item_color(color_id: Color) -> dict:
    return {"color_name": color_id.name}

# Path which uses a query param to filter items chepaer than max_price
@app.get("/items/")
async def get_cheap_items(max_price: float) -> list[Item]:
    return list(filter(lambda item: item.price < max_price, test_items))

# Path which uses path param, query param, and request body
# Path param gets item, query param filters item, request body gives update data
# Really don't need to pass in whole item here, but works for tutorial purposes
@app.patch("/items/{item_id}")
async def set_offer_if_item_expensive(item_id: int, item: Item, expensive_price: float) -> Item:
    for test_item in test_items:
        if test_item.id == item_id:
            if test_item.price > expensive_price:        
                test_item.is_offer = True
                test_item.price = item.price
                
            return test_item
        
    raise HTTPException(status_code=404, detail="Item not found")