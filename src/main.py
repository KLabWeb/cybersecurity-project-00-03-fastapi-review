# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()
]

# Most basic GET path
@app.get("/")
async def read_root():
    return {"Hello": "World"}