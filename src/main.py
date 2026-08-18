from app import app

# add middleware to app
import middleware.middleware

# add routes to app
import api.routes.item
import api.routes.file
import api.routes.purchase
import api.routes.root
import api.routes.user
import api.routes.wishlist

# add storage to app
from repository import init_storage

# init storage
@app.on_event("startup")
def on_startup():
    init_storage()