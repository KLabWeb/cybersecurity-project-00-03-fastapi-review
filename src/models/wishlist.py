from pydantic import BaseModel

class Wishlist(BaseModel):
    id: int
    user_id: int
    wishlist_item_ids: list[int]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 0,
                    "user_id": "0",
                    "item_id": "[0, 3, 5]",
                }
            ]
        }
    }
