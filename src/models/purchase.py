from pydantic import BaseModel


class Purchase(BaseModel):
    id: int
    user_id: int
    item_id: int
    manager_discount: bool | None = False
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 0,
                    "user_id": "0",
                    "item_id": "3",
                    "manager_discount": False
                }
            ]
        }
    }