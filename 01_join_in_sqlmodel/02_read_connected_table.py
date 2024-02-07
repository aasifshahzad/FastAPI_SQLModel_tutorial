
from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine,select
from dotenv import load_dotenv, find_dotenv
import os

_ : bool = load_dotenv(find_dotenv()) # read local .env file
db_key  = os.environ.get("CONN_STRING")
# print(db_key)


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

def create_heroes_without_optional_attributes():
    with Session(engine) as session:
        hero_Barde = Hero(name="Barde", secret_name="Dive Wilson", age=46)
        session.add(hero_Barde)
        session.commit()    
        session.refresh(hero_Barde)

        
        
def select_heroes_by_where():
    with Session(engine) as session:
        # statement = select(Hero).where(Hero.name == "Deadpond")
        statement = select(Hero).where(Hero.age > 40)
        heroes = session.exec(statement).all()
        print("Heroes: ", heroes)


def select_heroes_by_join_inner():
    with Session(engine) as session:
        statement = select(Hero).join(Team)
        heroes = session.exec(statement).all()
        print("Heroes_inner: ", heroes)

def select_heroes_by_join_left():
    with Session(engine) as session:
        statement = select(Hero).join(Team, isouter=True)
        heroes = session.exec(statement).all()
        print("Heroes_left: ", heroes)
        
def select_heroes_by_join_full():
    with Session(engine) as session:
        statement = select(Hero).join(Team, full=True)
        heroes = session.exec(statement).all()
        print("Heroes_full: ", heroes)


def main():
    # create_db_and_tables()
    # create_heroes_without_optional_attributes()
    # select_heroes_by_where()
    select_heroes_by_join_inner()
    select_heroes_by_join_left()
    select_heroes_by_join_full()



if __name__ == "__main__":
    main()
    print("Done")

