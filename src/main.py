from datetime import datetime
from fastapi import (
    FastAPI, 
    Body, 
    Cookie, 
    File, 
    Form, 
    Header, 
    HTTPException,
    Query, 
    UploadFile, 
    Path,
    Request
)
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Annotated, Any

from api.requests import (
    GetItemsQueryFilter,
    GetItemQueryFilter,
    CompareItemsPricesQueryFilter,
    PasswordVerificationUser,
    LoginFormRequest
)

from api.responses import (
    CreateSpooledFileResponse,
    GetItemResponse,
    UpdateItemResponse,
    GetPurchasesResponse,
    ItemPriceInfoMetadata,
    CompareItemPricesResponse,
    LoginFormResponse
)

from models.cookie import TrackingCookie
from models.exception import DangerousUserIDException
from models.header import RootHeader
from models.item import Item, Color, ItemID, UserID
from models.purchase import Purchase
from models.user import User

from repository import (
    get_item_by_id,
    get_items_by_id_range,
    get_items as get_all_items,
    put_item,
    get_purchases as get_all_purchases,
    get_purchases_by_user_id,
    put_purchase_from_item_and_user,
    get_user_by_id,
    get_user_by_username,
    authenticate_user,
    replace_item,
    update_item_color as repo_update_item_color
)


app = FastAPI()


### root endpoint ###


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


### Item endpoints ###

# Path which returns all items
# Slices return based on offest and limit from Query request filter
@app.get("/items")
async def get_items(
    filter_query: Annotated[GetItemsQueryFilter, Query()],
) -> list[Item]:
    return get_items_by_id_range(
        filter_query.offset, (filter_query.limit + filter_query.offset)
    )


# Path which gets two items using query param of list type via Query validation
# Obvisouly never define an endpoint like this (to just get two items) in a real system
@app.get("/items/price-comparison")
async def compare_item_prices(
    id: Annotated[CompareItemsPricesQueryFilter, Query()],
) -> CompareItemPricesResponse:
    current_datetime = datetime.now()
    
    first_item = get_item_by_id(id.id[0])
    second_item = get_item_by_id(id.id[1])
    
    if not first_item or not second_item:
        raise HTTPException(status_code=404, detail="One or both items not found")
    

    greater_price_item_id = (
        first_item.id
        if first_item.price > second_item.price
        else second_item.id if first_item.price < second_item.price else None
    )

    return CompareItemPricesResponse(
        item_price_info=[
            ItemPriceInfoMetadata(
                item_id=first_item.id,
                item_name=first_item.name,
                item_price=first_item.price,
                request_made=current_datetime,
            ),
            ItemPriceInfoMetadata(
                item_id=second_item.id,
                item_name=second_item.name,
                item_price=second_item.price,
                request_made=current_datetime,
            ),
        ],
        greater_price_item_id=greater_price_item_id,
    )
    
    
# Path takes path parameter to ID resource and get specific item
# ItemID carries the bounds validation via Path validation
# Regex Query validator checks if query has a least one letter
# Note how this endpoint also looks for a Cookie and Header being passed in w/ request
@app.get("/items/{item_id}")
async def get_item(
    item_id: Annotated[ItemID, Path()],
    q: Annotated[GetItemQueryFilter, Query()],
    last_item_id_viewed: Annotated[int | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
) -> GetItemResponse:
    existing_item = get_item_by_id(item_id)

    # Endpoint layer is in charge of HTTP communications in both responses & requests
    # As such, if an error occurs, like cannot find Item in repo, endpoint layer raises exception
    # And exception raised is in form that can be communicated via standard HTTP response
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    return GetItemResponse(
        item_id=existing_item.id,
        item_name=existing_item.name,
        query=q.q if q.q else None,
    )


# Path which creates item via request body details
@app.post("/items", status_code=201)
async def create_item(item: Item) -> Item:
    return put_item(item)


# Path which updates whole Item via request body details
# Also sets int to be embeded object inside request body
@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Annotated[Item, Body(embeded=True)]
) -> UpdateItemResponse:    
    updated_item = replace_item(item_id=item_id, item=item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")

    return UpdateItemResponse(
        item_id=updated_item.id,
        item_name=updated_item.name,
        color=updated_item.color,
        is_offer=updated_item.is_offer,
    )


# Path which only allows setting specific color names for updating color only
@app.patch("/items/{item_id}/color")
async def update_item_color(item_id: int, color: Color) -> Item:
    
    updated_item = repo_update_item_color(item_id=item_id, color=color)
    
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated_item


# Path which uses a query param to filter items chepaer than max_price
@app.get("/items/")
async def get_cheap_items(max_price: float) -> list[Item]:
    items = get_all_items()
    return list(filter(lambda item: item.price < max_price, items))


# Path which uses path param, query param, and request body
# Path param gets item, query param filters item, request body gives update data
# Really don't need to pass in whole item here, but works for tutorial purposes
@app.patch("/items/{item_id}")
async def set_offer_if_item_expensive(
    item_id: int, item: Item, expensive_price: float
) -> Item:
    existing_item = get_item_by_id(item_id)
    
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if existing_item.price > expensive_price:
        existing_item.is_offer = item.is_offer
        existing_item.price = item.price

    return existing_item


### Purchase endpoints ###

# Path which returns all purchases
@app.get("/purchases")
async def get_purchases() -> list[Purchase]:
    return get_all_purchases()


@app.get("/purchases/{user_id}")
async def get_purchases_by_user(user_id: int) -> GetPurchasesResponse:
    purchases = get_purchases_by_user_id(user_id=user_id)

    user_record = get_user_by_id(user_id=user_id)
    
    if not user_record:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"X-Error": "There goes my error"},
        )
                            
    items_purchased = []
    
    for purchase in purchases:
        item = get_item_by_id(purchase.item_id)
        if item is not None:
            items_purchased.append(item)

    return GetPurchasesResponse(user=User(**user_record.model_dump()), items_purchased=items_purchased)


# Path takes in two request bodies to create Purchase (an Item & User)
# Uses Body to pass in request body with only single primitive value
# Don't actually need two objects passed in here, as could just pass in IDs, but works for tutorial demo purposes
@app.put("/purchases", response_model=Purchase)
async def create_purchase_from_item_and_user(
    user: User, item: Item, manager_discount: Annotated[bool, Body()]
) -> Any:
    user_record = get_user_by_id(user_id=user.id)
    if not user_record:
        raise HTTPException(status_code=404, detail="User not found")
    
    item_record = get_item_by_id(item.id)
    if not item_record:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return put_purchase_from_item_and_user(user, item, manager_discount)

@app.get("/users/{user_id}")
async def get_user(user_id: Annotated[UserID, Path()]) -> User:
    existing_item = get_user_by_id(user_id)

    if not existing_item:
        raise HTTPException(status_code=404, detail="User not found")

    return existing_item

# Do not return a bool for auth like this but a Token, instead
# Not up to auth section in docs yet, so this works as a placeholder to demonstrate model inheritance section of docs
@app.post("/users/verify_auth")
async def verify_user_password(user: PasswordVerificationUser) -> bool:
    
    if not authenticate_user(user.id, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return True

# Path which reads in a Form and stores in memory
@app.post("/form_login")
async def login_via_form(form_data: Annotated[LoginFormRequest, Form()]) -> LoginFormResponse:
    user_record = get_user_by_username(form_data.username)

    if not user_record or not authenticate_user(user_record.id, form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return LoginFormResponse(username=form_data.username)

# Path which reads in a File
@app.post("/files")
async def create_file_in_memory(file: Annotated[bytes, File()]) -> dict[str, int]:
    return { "file_size": len(file)}

# Path which reads in a Spooled file (stored in mem until max size hit, then stored on local disk)
@app.post("/spooled_files/")
async def created_spooled_file(file: Annotated[UploadFile, File(description="Read in a spooled file")]) -> CreateSpooledFileResponse:
    first_part_of_file = await file.read(size=250)
    return CreateSpooledFileResponse(filename=file.filename, file_start_data=first_part_of_file)

# Custom exception handler for when getting an item but item is too dangerous
# Example: can occur in repository for get_item_by_id()
@app.exception_handler(DangerousUserIDException)
async def dangerous_id_exception_handler(request: Request, exc: DangerousUserIDException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Error: user id of '{exc.user_id}' for requested user is a dangerous id. Sorry, but we can't get this user."}
    )