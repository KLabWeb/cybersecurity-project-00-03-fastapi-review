# Single entry point for storage init, so callers (e.g. main.py) don't need
# to know which concrete backends exist behind the repository layer.
from repository.sql.db.sqlite import create_db_and_tables

def init_storage():
    create_db_and_tables()
    # Add other backends' init calls here as they're introduced.
