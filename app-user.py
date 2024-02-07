from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine
from dotenv import load_dotenv, find_dotenv
import os

_ : bool = load_dotenv(find_dotenv()) # read local .env file
db_key  = os.environ.get("CONN_STRING")
# print(db_key)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str 
    password: str
    roll: str
    age: Optional[int] = None
    

engine = create_engine(db_key, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def insert_dummy_data():
    with Session(engine) as session:
        session.add_all([
            User(name="John", email="john@example.com", password="password123", roll="student", age=20),
            User(name="Jane", email="jane@example.com", password="password456", roll="teacher", age=30),
            User(name="Bob", email="bob@example.com", password="password789", roll="admin", age=40),
        ])
        session.commit()
        print("Dummy data inserted successfully.")
        return True
    return False


if __name__ == "__main__":
    create_db_and_tables()
    insert_dummy_data()
