import time

from app import app

from fastapi import Request

# Middleware to determine request processing time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    
    response.headers["X-Process-Time"] = str(process_time)
    
    return response