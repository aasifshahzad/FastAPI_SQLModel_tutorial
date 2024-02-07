from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine
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

def create_heroes():
    #create Session
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")
        session.add(team_preventers)
        session.add(team_z_force)
        session.commit()
        session.refresh(team_preventers)
        session.refresh(team_z_force)
        
        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", age=42, team_id=team_preventers.id)
        hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team_id=team_z_force.id)
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.commit()    
        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)

def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
    print("Done")

