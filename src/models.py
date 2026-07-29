from pydantic import BaseModel
from enum import Enum

class Item(BaseModel):
    id: int
    name: str
    price: float
    is_offer: bool | None = None
    
class Color(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"