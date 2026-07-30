from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated, Literal


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


class ItemFilterQuery(BaseModel):
    limit: int = Field(100, gt=0, le=1000)
    offset: init = Field(0, ge=0)
    order_by: Literal