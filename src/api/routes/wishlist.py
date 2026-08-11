from app import app

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from api.dependencies.debug import DEBUGGER
from api.dependencies.fake_db import DB
from api.dependencies.header import SECRET_HEADER

from api.models.wishlist import WishlistDebugReponse

from repository.wishlist import get_whishlist_by_user_id

# Note the path operation decorator dependency here which returns nothing but still does something
# Check your response header values to see result of dependency being called
@app.get("/wishlists/{wishlist_id}", dependencies=[SECRET_HEADER])
async def get_wishlist(wishlist_id: int, db: DB, debugger: DEBUGGER, debug: bool = False) -> WishlistDebugReponse:
    existing_wishlist = db.get_wishlist_by_id(wishlist_id=wishlist_id)

    if existing_wishlist is None:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    return WishlistDebugReponse(wishlist=existing_wishlist, debug=debugger)


# Path operation which takes in a debugger dependency function
# Set debugger to 
@app.get("/wishlists/user/{user_id}")
async def get_wishlist_from_user_id(user_id: int, debugger: DEBUGGER, debug: bool = False) -> WishlistDebugReponse:
    existing_wishlist = get_whishlist_by_user_id(user_id)

    if existing_wishlist is None:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    return WishlistDebugReponse(wishlist=existing_wishlist, debug=debugger)


@app.exception_handler(ConnectionError)
async def db_connection_error_handler(request, exc):
    return JSONResponse(status_code=503, content={"detail": "Service temporarily unavailable"})
