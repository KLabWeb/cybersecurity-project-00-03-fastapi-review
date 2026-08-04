from pydantic import BaseModel

from models.item import Item
from models.user import User


class GetPurchasesResponse(BaseModel):
    user: User | None
    # List of models
    items_purchased: list[Item]
