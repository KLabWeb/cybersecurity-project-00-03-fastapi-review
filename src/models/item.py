from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated
from datetime import date


class Color(str, Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"


ItemID = Annotated[
    int,
    Field(
        description="ID of item. ID must be between 0 and 1,000,000.",
        ge=0,
        lt=1000000,
    ),
]


class Item(BaseModel):
    id: int
    name: str
    price: float
    color: Color | None = None
    is_offer: bool | None = None
    created_on: date
    updated_on: date
    tags: list[str] | None = None