from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv,find_dotenv
import os

_ : bool = load_dotenv(find_dotenv())
db_key = os.getenv("CONN_STRING")
print(os.getenv("CONN_STRING"))


def get_engine(db_key):
    engine = create_engine(db_key, echo=True)
    return engine

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

engine = get_engine(db_key)
print("Engine created successfully")
create_db_and_tables()
print("Database and tables created successfully")