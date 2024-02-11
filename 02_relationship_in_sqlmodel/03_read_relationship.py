
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

engine = create_engine(db_key, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_team():
    with Session(engine) as session:
        hero_bombo = Hero(name="Bombo", secret_name="Bom", age=36)
        hero_nambie = Hero(name="Nambie", secret_name="Namb", age=63)
        new_team = Team(
            name="Bombooos",
            headquarters="California",
            heroes=[hero_bombo, hero_nambie])
        session.add(new_team)
        session.commit()

def select_team():
    with Session(engine) as session:
        # statement = select(Team).where(Team.id == 1) # select by id
        statement = select(Team).where(Team.name == "Bombooos") # select by name
        results = session.exec(statement)
        team = results.first()
        print("Selected Team: ", team)
        print("Selected Team Heroes: ", team.heroes)



def main():
    # create_db_and_tables()
    # create_heroes_with_relationship()
    # create_team()
    select_team()



if __name__ == "__main__":
    main()
    print("Done")

