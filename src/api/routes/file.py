from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from api.models.files import CreateSpooledFileResponse

router = APIRouter(
    tags=["files"],
)


# Path which reads in a File
@router.post("/files")
async def create_file_in_memory(file: Annotated[bytes, File()]) -> dict[str, int]:
    return { "file_size": len(file)}


# Path which reads in a Spooled file (stored in mem until max size hit, then stored on local disk)
@router.post("/files/spooled-files")
async def created_spooled_file(file: Annotated[UploadFile, File(description="Read in a spooled file")]) -> CreateSpooledFileResponse:
    first_part_of_file = await file.read(size=250)
    return CreateSpooledFileResponse(filename=file.filename, file_start_data=first_part_of_file)
