from models.user import User
from pydantic import BaseModel, Field
from typing import Literal

class GetItemsQueryFilter(BaseModel):
    limit: int = Field(100, gt=0, le=1000)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"


class GetItemQueryFilter(BaseModel):
    q: str | None = Field(None,min_length=2, max_length=50, pattern="[a-zA-Z]")


class CompareItemsPricesQueryFilter(BaseModel):
    id: list[int] = Field(
        title="Size restricter query",
        description="Ensure 2 and only two item id are submitted for price comparison.",
        examples=[[1, 3]],
        alias="item_id",
        min_length=2,
        max_length=2,
    )


class PasswordVerificationUser(User):
    password: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
            {
                    "id": 2,
                    "username": "TomDickAndHarry",
                    "image": "http://www.tom-site.com",
                    "password": "badpassword"
                }
            ]
        }
    }