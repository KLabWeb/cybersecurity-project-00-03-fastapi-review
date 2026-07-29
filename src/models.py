from pydantic import BaseModel
from enum import Enum
    
class Color(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    
class Item(BaseModel):
    id: int
    name: str
    price: float
    color: Color | None = None
    is_offer: bool | None = None