from pydantic import BaseModel, HttpUrl


class User(BaseModel):
    id: int
    username: str
    image: HttpUrl | None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
            {
                    "id": 2,
                    "user_id": "TomDickAndHarry",
                    "image": "http://www.tom-site.com",
                }
            ]
        }
    }