from data.legacy.wishlist import raw_wishlists
from models.item import Item
from models.wishlist import Wishlist
from models.user import User

test_whishlists: list[Wishlist] = [
    Wishlist(**raw_wishlist) for raw_wishlist in raw_wishlists
]


def get_whishlist_by_id(wishlist_id: int) -> Wishlist | None:
    for wishlist in test_whishlists:
        if wishlist.id == wishlist_id:
            return wishlist

    return None


def get_whishlist_by_user_id(user_id: int) -> Wishlist | None:
    for wishlist in test_whishlists:
        if wishlist.user_id == user_id:
            return wishlist

    return None


def put_whishlist_from_items_and_user(user: User, item_ids: list[int]) -> Wishlist:
    wishlist_id = test_whishlists[-1].id + 1
    wishlist = Wishlist(
        id=wishlist_id,
        user_id=user.id,
        wishlist_item_ids=item_ids,
    )

    test_whishlists.append(wishlist)
    return wishlist
