from typing import Annotated
from fastapi import Depends, Response


async def get_secret_header(response: Response) -> None:
    response.headers["secret"] = "I am a secret header. I was built through a Depends path operator decorator executing."


SECRET_HEADER = Depends(get_secret_header)