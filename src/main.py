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

# apply items routes to app routes
app.include_router(item_router)

# init storage
@app.on_event("startup")
def on_startup():
    init_storage()