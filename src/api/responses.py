from models.item import Color, Item
from models.user import User

from pydantic import BaseModel


class ItemQueryResponse(BaseModel):
    item_id: int
    query: str | None = None


class ItemUpdateResponse(BaseModel):
    item_id: int
    item_name: str
    color: Color | None = None
    is_offer: bool | None = None
    
class GetPurchasesResponse(BaseModel):
    user: User
    items_purchased: list[Item]