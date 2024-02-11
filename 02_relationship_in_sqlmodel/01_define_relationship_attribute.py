
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine,select
from dotenv import load_dotenv, find_dotenv
import os

_ : bool = load_dotenv(find_dotenv()) # read local .env file
db_key  = os.environ.get("CONN_STRING")
# print(db_key)


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    headquarters: str
    heroes: list["Hero"] = Relationship(back_populates="team")
    
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heroes")

engine = create_engine(db_key, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_heroes_with_relationship():
    with Session(engine) as session:
        team_fighter = Team(name="Fighters", headquarters="Shanghai")
        team_rogue = Team(name="Rogues", headquarters="Beijing")
        
        hero_naste = Hero(name="Naste", secret_name="Nas", team=team_fighter)
        hero_ryu = Hero(name="Ryu", secret_name="Ryu", team=team_rogue)
        
        session.add_all([team_fighter, team_rogue, hero_naste, hero_ryu])
        session.commit()



def main():
    # create_db_and_tables()
    create_heroes_with_relationship()



if __name__ == "__main__":
    main()
    print("Done")

