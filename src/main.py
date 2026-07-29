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

# Most basic GET path
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Path takes path parameter to ID resource
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

# Path which takes in Item as request body
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id, "test": item.mixed_type_tuple}

# Path which only allows getting specific color names
@app.get("/item-color/{color_id}")
async def get_color(color_id: Color):
    return {"color_name": color_id.name}