from sqlmodel import Field, select, SQLModel
from typing import Sequence

from models.exception import PurchaseNotFoundException
from models.purchase import Purchase as DomainPurchase
from repository.sql.db.sqlite import SQL_SESSION


class PurchaseBase(SQLModel):
    """Base class (shared fields)"""

    user_id: int
    item_id: int
    manager_discount: bool | None = False


class Purchase(PurchaseBase, table=True):
    """DB model class"""

    id: int | None = Field(default=None, primary_key=True, index=True)
    secret_tracking_id: str


class PurchaseCreate(PurchaseBase):
    """Creation class - allows client to submit secrect_tracking_id
    but not id, as id should only be set by DB"""

    secret_tracking_id: str


class PurchaseUpdate(SQLModel):
    """Inherits from SQLModel and not PurchaseBase as inheriting from Purchasebase then giving same name props would break liskov substitution principle"""

    user_id: int | None = None
    item_id: int | None = None
    manager_discount: bool | None = False


def translate_purchase_to_domain(purchase: Purchase) -> DomainPurchase:
    return DomainPurchase(**purchase.model_dump())


def translate_purchases_to_domain(
    purchases: Sequence[Purchase],
) -> list[DomainPurchase]:
    return [translate_purchase_to_domain(purchase) for purchase in purchases]


async def create_purchase(
    sql_session: SQL_SESSION, purchase: PurchaseCreate
) -> DomainPurchase:
    db_purchase = Purchase.model_validate(purchase)

    sql_session.add(db_purchase)
    sql_session.commit()
    sql_session.refresh(db_purchase)  # necessary for purchase object not to be stale

    return translate_purchase_to_domain(db_purchase)


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


async def update_purchase(
    purchase_id: int, purchase_update: PurchaseUpdate, sql_session: SQL_SESSION
) -> DomainPurchase:
    purchase_record = sql_session.get(Purchase, purchase_id)

    if not purchase_record:
        raise PurchaseNotFoundException(purchase_id=purchase_id)

    # do not set values for purchase_update probs with no values set
    purchase_update_data = purchase_update.model_dump(exclude_unset=True)
    purchase_record.sqlmodel_update(purchase_update_data)

    sql_session.add(purchase_record)
    sql_session.commit()
    sql_session.refresh(purchase_record)

    purchase = translate_purchase_to_domain(purchase_record)
    return purchase


async def delete_purchase(purchase_id: int, sql_session: SQL_SESSION) -> DomainPurchase:
    purchase = sql_session.get(Purchase, purchase_id)

    if not purchase:
        raise PurchaseNotFoundException(purchase_id=purchase_id)

    domain_purchase = translate_purchase_to_domain(purchase)

    sql_session.delete(purchase)
    sql_session.commit()

    return domain_purchase
