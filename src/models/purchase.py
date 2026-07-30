from pydantic import BaseModel


class Purchase(BaseModel):
    id: int
    user_id: int
    item_id: int