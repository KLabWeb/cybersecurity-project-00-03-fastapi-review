from models.wishlist import Wishlist
from random import randint
from typing import Annotated, AsyncGenerator
from unittest.mock import MagicMock as DBSession

from fastapi import Depends

from repository.wishlist import test_whishlists

async def get_db() -> AsyncGenerator[DBSession, None]:
    db = DBSession()
    db = config_db(db)
    
    try:
        potential_connection_lost = randint(0, 4)
        if potential_connection_lost == 0:
            raise ConnectionError("Failed to connect to DB.")
        yield db
    except ConnectionError:
        raise
    finally:
        db.close()
    
        
def config_db(db: DBSession) -> DBSession:
    db.wishlists = test_whishlists
    
    db.get_wishlist_by_id = lambda wishlist_id: next(
        (w for w in db.wishlists if w.id == wishlist_id), None
    )

    return db        
        

DB = Annotated[DBSession, Depends(get_db)]

