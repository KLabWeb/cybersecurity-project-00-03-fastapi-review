from sqlmodel import Field, SQLModel

from repository.sql.db.sqlite import SQL_SESSION


class Purchase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    item_id: int
    manager_discount: bool | None = False


async def create_purchase(purchase: Purchase, sql_session: SQL_SESSION) -> Purchase:
    sql_session.add(purchase)
    sql_session.commit()
    sql_session.refresh(purchase)
    return purchase
