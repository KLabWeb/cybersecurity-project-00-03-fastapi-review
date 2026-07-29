from pydantic import BaseModel

class ItemQueryResponse(BaseModel):
    item_id: int
    query: str | None = None
    
class ItemUpdateResponse(BaseModel):
    item_id: int
    item_name: str
    is_offer: bool | None = None