# Raw wishlist data for the legacy store
# Plain values only - the repository layer defines the model and builds from these
raw_wishlists: list[dict] = [
    {"id": 0, "user_id": 0, "wishlist_item_ids": [0, 2, 3]},
    {"id": 1, "user_id": 1, "wishlist_item_ids": [1, 2]},
    {"id": 2, "user_id": 0, "wishlist_item_ids": [1]},
    {"id": 3, "user_id": 3, "wishlist_item_ids": [1, 2, 3]},
    {"id": 4, "user_id": 1, "wishlist_item_ids": [0, 1, 2, 3]},
    {"id": 5, "user_id": 0, "wishlist_item_ids": []},
    {"id": 6, "user_id": 0, "wishlist_item_ids": [0, 1, 2]},
]
