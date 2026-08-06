from fastapi import Depends
from typing import Annotated

from api.models.debug import WishlistDebug


def get_debug(debug: bool = False) -> WishlistDebug | None:
    return WishlistDebug(debug=debug) if debug else None


DEBUGGER = Annotated[WishlistDebug | None, Depends(get_debug)]
