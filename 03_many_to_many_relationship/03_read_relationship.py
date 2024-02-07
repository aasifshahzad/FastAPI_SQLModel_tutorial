
from typing import Optional
from sqlalchemy import update
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine,select
from dotenv import load_dotenv, find_dotenv
import os

_ : bool = load_dotenv(find_dotenv()) # read local .env file
db_key  = os.environ.get("CONN_STRING")
# print(db_key)

class HeroTeamLink(SQLModel, table=True):
    hero_id: Optional[int] = Field(default= None, foreign_key="hero.id", primary_key=True)
    team_id: Optional[int] = Field(default= None, foreign_key="team.id", primary_key=True)

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    headquarters: str
    heroes: list["Hero"] = Relationship(back_populates="team", link_model=HeroTeamLink)

    

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    team: Optional["Team"] = Relationship(back_populates="heroes", link_model=HeroTeamLink)


engine = create_engine(db_key, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine,)
    
def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            teams=[team_z_force, team_preventers],
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            teams=[team_preventers],
        )
        hero_spider_boy = Hero(
            name="Spider-Boy", secret_name="Pedro Parqueador", teams=[team_preventers]
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Deadpond:", hero_deadpond)
        print("Deadpond teams:", hero_deadpond.team)
        print("Rusty-Man:", hero_rusty_man)
        print("Rusty-Man Teams:", hero_rusty_man.team)
        print("Spider-Boy:", hero_spider_boy)
        print("Spider-Boy Teams:", hero_spider_boy.team)


def main():
    create_db_and_tables()
    create_heroes()
    



if __name__ == "__main__":
    main()
    print("Done")

