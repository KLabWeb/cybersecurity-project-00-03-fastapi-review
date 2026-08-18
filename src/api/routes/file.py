from typing import Annotated

from fastapi import File, UploadFile

from app import app
from api.models.files import CreateSpooledFileResponse


# Path which reads in a File
@app.post("/files")
async def create_file_in_memory(file: Annotated[bytes, File()]) -> dict[str, int]:
    return { "file_size": len(file)}


# Path which reads in a Spooled file (stored in mem until max size hit, then stored on local disk)
@app.post("/spooled_files/")
async def created_spooled_file(file: Annotated[UploadFile, File(description="Read in a spooled file")]) -> CreateSpooledFileResponse:
    first_part_of_file = await file.read(size=250)
    return CreateSpooledFileResponse(filename=file.filename, file_start_data=first_part_of_file)
