from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

from models.item import Color


class GetItemsQueryFilter(BaseModel):
    limit: int = Field(100, gt=0, le=1000)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"


class GetItemQueryFilter(BaseModel):
    q: str | None = Field(None, min_length=2, max_length=50, pattern="[a-zA-Z]")


class CompareItemsPricesQueryFilter(BaseModel):
    id: list[int] = Field(
        title="Size restricter query",
        description="Ensure 2 and only two item id are submitted for price comparison.",
        examples=[[1, 3]],
        alias="item_id",
        min_length=2,
        max_length=2,
    )


class GetItemResponse(BaseModel):
    item_id: int
    item_name: str
    query: str | None = None


class UpdateItemResponse(BaseModel):
    item_id: int
    item_name: str
    color: Color | None = None
    is_offer: bool | None = None


class ItemPriceInfo(BaseModel):
    item_id: int
    item_name: str
    item_price: float


class ItemPriceInfoMetadata(ItemPriceInfo):
    request_made: datetime


class CompareItemPricesResponse(BaseModel):
    # Model within model
    item_price_info: list[ItemPriceInfoMetadata]
    greater_price_item_id: int | None = None


class ItemActionTags(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"