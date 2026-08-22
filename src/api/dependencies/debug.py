from fastapi import Depends, Request
from typing import Annotated

from api.models.debug import WishlistDebug, IPDebugResponse

from repository.legacy.banned_host import get_banned_hosts


def get_debug(debug: bool = False) -> WishlistDebug | None:
    return WishlistDebug(debug=debug) if debug else None


class GetDebug:
    def __init__(self, banned_hosts: frozenset[str]):
        self.banned_hosts = banned_hosts

    def __call__(self, request: Request, debug: bool = False) -> IPDebugResponse | None:
        if not debug or not request.client:
            return None

        host = request.client.host
        banned_ip = host in self.banned_hosts
        
        return IPDebugResponse(client_ip=host, banned_ip=banned_ip)
        
IP_DEBUGGER = Annotated[IPDebugResponse | None, Depends(GetDebug(get_banned_hosts()))]        

GENERAL_DEBUGGER = Annotated[WishlistDebug | None, Depends(get_debug)]