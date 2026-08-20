from sqlmodel import Field, select, SQLModel
from typing import Annotated, Sequence

from models.purchase import Purchase as DomainPurchase
from repository.sql.db.sqlite import SQL_SESSION


class Purchase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    user_id: int
    item_id: int
    manager_discount: bool | None = False


def translate_purchase_to_domain(purchase: Purchase) -> DomainPurchase:
    return DomainPurchase(**purchase.model_dump())


def translate_purchases_to_domain(
    purchases: Sequence[Purchase],
) -> list[DomainPurchase]:
    return [translate_purchase_to_domain(purchase) for purchase in purchases]


async def create_purchase(
    sql_session: SQL_SESSION, purchase: Purchase
) -> DomainPurchase:
    sql_session.add(purchase)
    sql_session.commit()
    sql_session.refresh(purchase)  # necessary for purchase object not to be stale
    return translate_purchase_to_domain(purchase)


async def get_purchase(
    sql_session: SQL_SESSION, purchase_id: int
) -> DomainPurchase | None:
    purchase = sql_session.get(Purchase, purchase_id)
    
    if purchase:
        return translate_purchase_to_domain(purchase)

    return None


async def get_purchases(
    sql_session: SQL_SESSION, offset: int, limit: int
) -> list[DomainPurchase]:
    statement = select(Purchase)  # get sql statement
    statement = statement.offset(offset)  # get updated statement w/ offset
    statement = statement.limit(limit)  # get updated statement w/ limit

    result = sql_session.exec(statement)  # excecute sql statement

    return translate_purchases_to_domain(result.all())  # return all rows
