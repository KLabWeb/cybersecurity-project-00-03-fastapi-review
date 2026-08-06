import uuid
from datetime import datetime
from pydantic import BaseModel

class WishlistDebug(BaseModel):
    debug: bool = False
    date_time: datetime = datetime.now()
    trace_id: str = str(uuid.uuid4())
    note: str = "fake debug data for practicing Depends"
