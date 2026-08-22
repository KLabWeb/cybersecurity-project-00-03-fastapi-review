from pydantic import BaseModel

from models.wishlist import Wishlist
from api.models.debug import IPDebugResponse, WishlistDebug


class WishlistDebugReponse(BaseModel):
    wishlist: Wishlist
    debug: WishlistDebug | None


class WishlistIPDebugResponse(WishlistDebugReponse):
    ip_debug: IPDebugResponse | None = None