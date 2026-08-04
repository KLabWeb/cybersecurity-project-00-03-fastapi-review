from typing import Annotated

from fastapi import Cookie, Header
from fastapi.responses import RedirectResponse

from app import app
from models.cookie import TrackingCookie
from models.header import RootHeader


# Most basic GET path to get root of API
# Takes in ookie model and Header model
@app.get("/")
async def get_root(
    tracking_cookie: Annotated[TrackingCookie, Cookie()],
    header: Annotated[RootHeader, Header()],
) -> dict[str, str]:
    return {"Hello": "World"}


# Response re-directs to another URL
@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
