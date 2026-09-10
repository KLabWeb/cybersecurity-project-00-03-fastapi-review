from typing import Annotated

from fastapi import APIRouter, Cookie, Header, Request
from fastapi.responses import RedirectResponse

from models.cookie import TrackingCookie
from models.header import RootHeader

router = APIRouter(
    tags=["root"],
)

# Most basic GET path to get root of API
# Takes in ookie model and Header model
@router.get("/")
async def get_root(
    tracking_cookie: Annotated[TrackingCookie, Cookie()],
    header: Annotated[RootHeader, Header()],
    request: Request,
) -> dict:
    return {
        "msg": "Hello, world",
        "root_path": request.scope.get("root_path")
    }


# Response re-directs to another URL
@router.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
