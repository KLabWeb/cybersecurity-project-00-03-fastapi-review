from pydantic import BaseModel

class RootHeader(BaseModel):
    model_config = {"extra": "forbid"}
    
    host: str | None = None
    save_data: bool | None = None
    if_modified_since: str | None = None