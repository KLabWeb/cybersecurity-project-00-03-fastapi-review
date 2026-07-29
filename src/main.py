# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None
    mixed_type_tuple: tuple[int, int, str] | None = None
    name_to_num: dict[str, int] | None = None
    
class Color(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    
test_items: list[Item] = [
    Item(name="Apple", price=0.41, is_offer=True),
    Item(name="Pear", price=0.49, is_offer=False),
    Item(name="Pineapple", price=2.49, is_offer=False),
    Item(name="Peach", price=0.57, is_offer=False)
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
async def get_color(color_id: Color):
    return {"color_name": color_id.name}

# Path which uses a query param to filter items chepaer than max_price
@app.get("/items/")
async def get_cheap_items(max_price: float):
    return list(filter(lambda item: item.price < max_price, test_items))