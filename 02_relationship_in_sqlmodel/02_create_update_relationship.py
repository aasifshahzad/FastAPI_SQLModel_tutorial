
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

# def create_heroes_with_relationship():
#     with Session(engine) as session:
#         statement_1 = select(Team).where(Team.name == "Preventers")
#         team = session.exec(statement_1).first()
#         statement_2 = select(Hero).where(Hero.name == "Ryu")
#         hero = session.exec(statement_2).first()
#         hero.team = team
#         session.add(hero)
#         session.commit()
#         session.refresh(hero)   
        


def create_heroes_with_relationship():
    with Session(engine) as session:
        statement_1 = select(Team).where(Team.name == "	Fighters")
        team = session.exec(statement_1).first()
        statement_2 = select(Hero).where(Hero.name == "Deadpond")
        hero = session.exec(statement_2).first()
        hero.team = team
        session.add(hero)
        session.commit()
        session.refresh(hero)  
        
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
        



def main():
    # create_db_and_tables()
    # create_heroes_with_relationship()
    create_team()



if __name__ == "__main__":
    main()
    print("Done")

