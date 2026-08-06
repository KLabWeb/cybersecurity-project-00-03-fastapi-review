from pydantic import BaseModel

from models.wishlist import Wishlist
from api.models.debug import WishlistDebug


class WishlistDebugReponse(BaseModel):
    wishlist: Wishlist
    debug: WishlistDebug | None
