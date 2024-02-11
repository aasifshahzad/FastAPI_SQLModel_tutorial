from sqlmodel import Session, select
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Annotated

from database import create_db_and_tables
from depend import get_session
from models import Hero, HeroCreate, HeroResponse, UpdateHero, Team, TeamBase, TeamCreate, TeamResponse, TeamUpdate


app : FastAPI = FastAPI()

#API with Dependency injection

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "Your App is Running ;-)"}

#Get all Heroes
@app.get("/heroes", response_model=list[Hero] | None, tags=["heroes"]) 
# # Static pagination
# def get_heroes(session: Annotated[Session, Depends(get_session)]): # Dependencies injection
#     heroes = session.exec(select(Hero).offset(0).limit(2)).all() 
#     return heroes

# #Dynamic Pagination
# def get_heroes(session: Annotated[Session, Depends(get_session)], offset :int = 0, limit: int = 2): # Dependencies injection
#     heroes = session.exec(select(Hero).offset(offset).limit(limit)).all() # Static pagination
#     return heroes


#Dynamic Pagination with max and min using Query
def get_heroes(session: Annotated[Session, Depends(get_session)], offset :int = Query(default=0, le=4), limit: int = Query(default=2, le=4)): # Dependencies injection
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all() # Static pagination
    return heroes

#Create Heroes
@app.post("/heroes", response_model=HeroResponse, tags=["heroes"]) # HeroResponse model
def create_hero(hero: HeroCreate, db: Annotated[Session, Depends(get_session)]):# HeroCreate model
    print("Data from Client", hero)
    hero_to_insert = Hero.model_validate(hero) #Mapping the createHero class with Hero class
    print("Data after validation", hero_to_insert)
    db.add(hero_to_insert)
    db.commit()
    db.refresh(hero_to_insert)
    return hero_to_insert

#single hero by name
@app.get("/heroes/{hero_name}", response_model=HeroResponse, tags=["heroes"])
def get_hero(hero_name: str, db: Annotated[Session, Depends(get_session)]):
    hero = db.exec(select(Hero).where(Hero.name == hero_name)).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


#Update Heroes with all tp update at once
@app.put("/heroes/{hero_id}", response_model=HeroResponse, tags=["heroes"])
def update_all_hero(hero_id: int, hero: HeroCreate, db: Annotated[Session, Depends(get_session)]):
    hero_to_update = db.exec(select(Hero).where(Hero.id == hero_id)).first()
    hero_to_update.name = hero.name
    hero_to_update.secret_name = hero.secret_name
    hero_to_update.age = hero.age
    
    db.commit()
    db.refresh(hero_to_update)
    return hero_to_update

@app.patch("/heroes/{hero_id}", tags=["heroes"])
def update_hero_single_value(hero_id: int, hero_data: UpdateHero, db: Session = Depends(get_session)):
    hero = db.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    #Update Hero
    print("Hero in DB:", hero)
    print("Hero Data from client:", hero_data)
    
    hero_dict_data = hero_data.model_dump(exclude_unset= True)
    print("Hero Dict Data:", hero_dict_data)
    
    for key, value in hero_dict_data.items():
        setattr(hero, key, value)
    print("Hero after update:", hero)
    
    db.add(hero)
    db.commit()
    db.refresh(hero)
    
    return hero
    
@app.delete("/heroes/{hero_id}", tags=["heroes"])
def delete_hero(hero_id: int, db: Session = Depends(get_session)):
    hero = db.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    db.delete(hero)
    db.commit()
    return {"message": "Hero deleted successfully"}     
    




# Get all teams with dynamic pagination
@app.get("/teams", response_model=list[TeamResponse], tags=["teams"])
def get_teams(session: Session = Depends(get_session), offset: int = Query(default=0, le=4), limit: int = Query(default=2, le=4)):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams

# Create a new team
@app.post("/teams", response_model=TeamResponse, tags=["teams"])
def create_team(team: TeamCreate, session: Session = Depends(get_session)):
    team_to_create = Team(**team.dict())
    session.add(team_to_create)
    session.commit()
    session.refresh(team_to_create)
    return team_to_create

# Get a single team by ID
@app.get("/teams/{team_id}", response_model=TeamResponse, tags=["teams"])
def get_team(team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# Update a team by ID
@app.put("/teams/{team_id}", response_model=TeamResponse, tags=["teams"])
def update_team(team_id: int, team: TeamUpdate, session: Session = Depends(get_session)):
    team_to_update = session.get(Team, team_id)
    if not team_to_update:
        raise HTTPException(status_code=404, detail="Team not found")

    for attr, value in team.dict(exclude_unset=True).items():
        setattr(team_to_update, attr, value)

    session.commit()
    session.refresh(team_to_update)
    return team_to_update

# Delete a team by ID
@app.delete("/teams/{team_id}", tags=["teams"])
def delete_team(team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"message": "Team deleted successfully"}
