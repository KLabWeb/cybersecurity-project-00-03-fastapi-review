from models.item import Color, Item
from models.user import User

from pydantic import BaseModel


class GetItemResponse(BaseModel):
    item_id: int
    item_name: str
    query: str | None = None


class UpdateItemResponse(BaseModel):
    item_id: int
    item_name: str
    color: Color | None = None
    is_offer: bool | None = None
    
class GetPurchasesResponse(BaseModel):
    user: User
    # List of models
    items_purchased: list[Item]
    
    
class ItemPriceInfo(BaseModel):
    item_id: int
    item_name: str
    item_price: float
       
class CompareItemPricesResponse(BaseModel):
    # Model within model
    item_price_info: list[ItemPriceInfo]
    greater_price_item_id: int | None = None