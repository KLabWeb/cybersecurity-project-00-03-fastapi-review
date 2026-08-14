from pydantic import BaseModel, HttpUrl

class User(BaseModel):
    id: int
    username: str
    image: HttpUrl | None = HttpUrl(url="http://mysite.com/my_image.jpg")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
            {
                    "id": 2,
                    "username": "TomDickAndHarry",
                    "image": "http://www.tom-site.com",
                }
            ]
        }
    }
    

class Token(BaseModel):
    access_token: str
    token_type: str