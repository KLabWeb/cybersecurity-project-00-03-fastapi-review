from pydantic import BaseModel


class CreateSpooledFileResponse(BaseModel):
    filename: str | None
    file_start_data: bytes
