from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


# Plane Model classes for fastapi and pydantic

# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     secret_name: str
#     age: int | None = None

# class HeroCreate(SQLModel):
#     name: str
#     secret_name: str
#     age: int | None = None
    
# class HeroResponse(SQLModel):
#     id: int
#     name: str
#     secret_name: str
#     age: int | None = None


# Classes with inheritance
class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    age: int | None = None
    teams: List["Team"] = Relationship(back_populates="heroes")

class HeroCreate(HeroBase):
    age: int | None = None

class HeroResponse(HeroBase):
    id: int
    age: int | None = None


class UpdateHero(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str
    
class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    heroes: List["Hero"] = Relationship(back_populates="teams")

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int
    heroes: List["Hero"] = []
    
class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None
    heroes: List[Hero] | None = None
    