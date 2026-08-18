# Single entry point for storage init, so callers (e.g. main.py) don't need
# to know which concrete backends exist behind the repository layer.
from repository.sql.db.sqlite import create_db_and_tables as _init_sql

def init_storage():
    _init_sql()
    # Add other backends' init calls here as they're introduced.
