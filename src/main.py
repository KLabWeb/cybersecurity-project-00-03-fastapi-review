from app import app

# add middleware to app
import middleware.middleware

# add routes to app via @app route imports
import api.routes.item
import api.routes.file
import api.routes.purchase
import api.routes.root
import api.routes.user
import api.routes.wishlist

# add routes to app via APIRouter
from api.routes.item import router as item_router

# add storage to app
from repository import init_storage

# to allow debugging
import debugpy
import os

# apply items routes to app routes
app.include_router(item_router)

if os.getenv("DEBUG") == "1":
    debugpy.listen(("0.0.0.0", 5678))
    if os.getenv("DEBUG_WAIT") == "1":
        debugpy.wait_for_client()

# init storage
@app.on_event("startup")
def on_startup():
    init_storage()