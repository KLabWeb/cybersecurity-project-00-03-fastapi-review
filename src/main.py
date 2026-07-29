# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float
    is_offer: bool | None = None
    
class Color(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    
test_items: list[Item] = [
    Item(id=1, name="Apple", price=0.41, is_offer=True),
    Item(id=2, name="Pear", price=0.49, is_offer=False),
    Item(id=3, name="Pineapple", price=2.49, is_offer=False),
    Item(id=4, name="Peach", price=0.57, is_offer=False)
]
    
# Most basic GET path
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Path which returns all items
@app.get("/items")
async def read_items() -> list[Item]:
    return test_items

# Path takes path parameter to ID resource
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# Path which creates item via request body details
@app.post("/items/{item_id}")
async def create_item(item: Item) -> Item:
    test_items.append(item)
    return item

# Path which updates whole Item via request body details
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "is_offer": item.is_offer}

# Path which only allows getting specific color names
@app.get("/item-color/{color_id}")
async def get_item_color(color_id: Color):
    return {"color_name": color_id.name}

# Path which uses a query param to filter items chepaer than max_price
@app.get("/items/")
async def get_cheap_items(max_price: float):
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