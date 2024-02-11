from sqlmodel import Session, select
from database import create_db_and_tables, engine
from models import Hero
from fastapi import FastAPI

# Plain API without Dependency injection

app : FastAPI = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Your App is Running ;-)"}

#Get all Heroes
@app.get("/heroes", response_model=list[Hero] | None, tags=["heroes"])
def get_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes

#Create Heroes
@app.post("/heroes", response_model=Hero, tags=["heroes"])
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero





def create_heroes():
    with Session(engine) as session:
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team=team_z_force
        )
        session.add(hero_deadpond)
        session.commit()

        session.refresh(hero_deadpond)

        print("Created hero:", hero_deadpond)
        print("Hero's team:", hero_deadpond.team)


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()