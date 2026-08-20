from typing import Annotated, Any

from fastapi import Body, HTTPException, Query

from app import app
from api.models.purchases import GetPurchasesResponse
from models.exception import PurchaseNotFoundException
from models.item import Item
from models.purchase import Purchase
from models.user import User

from repository.legacy.item import get_item_by_id
from repository.legacy.purchase import get_purchases_by_user_id
from repository.legacy.user import get_user_by_id

from repository.sql.db.sqlite import SQL_SESSION
from repository.sql.models.purchase import create_purchase, PurchaseCreate, delete_purchase as delete_sql_purchase, get_purchase as get_sql_purchase, get_purchases as get_sql_purchases


# Path which returns all purchases
# Uses limit and offset to paginate results
@app.get("/purchases")
async def get_purchases(
    sql_session: SQL_SESSION,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
) -> list[Purchase]:
    
    return await get_sql_purchases(offset=offset, limit=limit, sql_session=sql_session)


@app.get("/users/purchases/{purchase_id}")
async def get_purchase(purchase_id: int, sql_session: SQL_SESSION) -> Purchase:
    purchase = await get_sql_purchase(purchase_id=purchase_id, sql_session=sql_session)

    if not purchase: 
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    return purchase

# Endpoint which raises custom headers and detail if exception hit
# returns response object after building response from two repo queries
@app.get("/purchases/user/{user_id}")
async def get_purchases_by_user(user_id: int) -> GetPurchasesResponse:
    purchases = get_purchases_by_user_id(user_id=user_id)

    user = get_user_by_id(user_id=user_id)

    if user is None:
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

    return GetPurchasesResponse(user=user, items_purchased=items_purchased)


# Path takes in two request bodies to create Purchase (an Item & User)
# Uses Body to pass in request body with only single primitive value
# Don't actually need two objects passed in here, as could just pass in IDs, but works for tutorial demo purposes
@app.put("/purchases", response_model=Purchase)
async def create_purchase_from_item_and_user(
    user: User,
    item: Item,
    manager_discount: Annotated[bool, Body()],
    secret_tracking_id: str,
    sql_session: SQL_SESSION,
) -> Purchase:
    user_record = get_user_by_id(user_id=user.id)
    if user_record is None:
        raise HTTPException(status_code=404, detail="User not found")

    item_record = get_item_by_id(item.id)
    if item_record is None:
        raise HTTPException(status_code=404, detail="Item not found")

    purchase = PurchaseCreate(
        user_id=user_record.id,
        item_id=item_record.id,
        manager_discount=manager_discount,
        secret_tracking_id=secret_tracking_id,
    )

    return await create_purchase(purchase=purchase, sql_session=sql_session)

@app.delete("/purchases")
async def delete_purchase(purchase_id: int, sql_session: SQL_SESSION) -> Purchase:
    try:
        purchase = await delete_sql_purchase(purchase_id=purchase_id, sql_session=sql_session)
    except PurchaseNotFoundException:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    return purchase