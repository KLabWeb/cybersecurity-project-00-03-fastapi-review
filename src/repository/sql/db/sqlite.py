from typing import Annotated

from fastapi import Depends

from sqlmodel import create_engine, Session, SQLModel

SQLITE_FILE_NAME =  "database.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

CONNECT_ARGS = {"check_same_thread": False}
ENGINE = create_engine(SQLITE_URL, connect_args=CONNECT_ARGS)

def create_db_and_tables():
    SQLModel.metadata.create_all(ENGINE)
    
def get_session():
    with Session(ENGINE) as session:
        yield session
        
SQL_SESSION = Annotated[Session, Depends(get_session)]