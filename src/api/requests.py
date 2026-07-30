from pydantic import BaseModel, Field
from typing import Literal


class GetItemsQueryFilter(BaseModel):
    limit: int = Field(100, gt=0, le=1000)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


class GetItemQueryFilter(BaseModel):
    q: str | None = Field(min_length=2, max_length=50, pattern="[a-zA-Z]")


class GetTwoItemsQueryFilter(BaseModel):
    id: list[int] = Field(
        title="Size restricter query",
        description="Ensure 2 and only 2 id are requested",
        alias="get-too",
        min_length=2,
        max_length=2,
    )
