from pydantic import BaseModel
from models import Color

class ItemQueryResponse(BaseModel):
    item_id: int
    query: str | None = None
    
class ItemUpdateResponse(BaseModel):
    item_id: int
    item_name: str
    color: Color | None = None
    is_offer: bool | None = None
    