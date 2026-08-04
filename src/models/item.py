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

UserID = Annotated[
    int,
    Field(
        description="ID of user. ID must be between 0 and 1,000,000.",
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
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 0,
                    "name": "Apple",
                    "price": "0.49",
                    "color": "red",
                    "is_offer": False,
                    "created_on": "2026-01-17",
                    "updated_on": "2026-05-22",
                }
            ]
        }
    }