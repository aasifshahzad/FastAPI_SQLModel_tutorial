from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine
from dotenv import load_dotenv, find_dotenv
import os

_ : bool = load_dotenv(find_dotenv()) # read local .env file
db_key  = os.environ.get("CONN_STRING")
print(db_key)


class Team(SQLModel, table=True):
    """
    
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    headquarters: str
    
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


engine = create_engine(db_key, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def main():
    create_db_and_tables()


if __name__ == "__main__":
    create_db_and_tables()
    print("Done")

