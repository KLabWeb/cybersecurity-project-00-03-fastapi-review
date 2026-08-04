from typing import Annotated, Any

from fastapi import Body, HTTPException

from app import app
from api.models.purchases import GetPurchasesResponse
from models.item import Item
from models.purchase import Purchase
from models.user import User
from repository.item import get_item_by_id
from repository.purchase import (
    get_purchases as get_all_purchases,
    get_purchases_by_user_id,
    put_purchase_from_item_and_user,
)
from repository.user import get_user_by_id


# Path which returns all purchases
@app.get("/purchases")
async def get_purchases() -> list[Purchase]:
    return get_all_purchases()


@app.get("/purchases/{user_id}")
async def get_purchases_by_user(user_id: int) -> GetPurchasesResponse:
    purchases = get_purchases_by_user_id(user_id=user_id)

    user_record = get_user_by_id(user_id=user_id)

    if user_record is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"X-Error": "There goes my error"},
        )

    items_purchased = []

    for purchase in purchases:
        item = get_item_by_id(purchase.item_id)
        if item is not None:
            items_purchased.append(item)

    return GetPurchasesResponse(user=User(**user_record.model_dump()), items_purchased=items_purchased)


# Path takes in two request bodies to create Purchase (an Item & User)
# Uses Body to pass in request body with only single primitive value
# Don't actually need two objects passed in here, as could just pass in IDs, but works for tutorial demo purposes
@app.put("/purchases", response_model=Purchase)
async def create_purchase_from_item_and_user(
    user: User, item: Item, manager_discount: Annotated[bool, Body()]
) -> Any:
    user_record = get_user_by_id(user_id=user.id)
    if user_record is None:
        raise HTTPException(status_code=404, detail="User not found")

    item_record = get_item_by_id(item.id)
    if item_record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return put_purchase_from_item_and_user(user, item, manager_discount)
