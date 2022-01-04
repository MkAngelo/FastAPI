# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl, PositiveInt

# FastAPI
from fastapi import status
from fastapi import FastAPI, Body, Query, Path, Form

app = FastAPI()

# Models

class HairColor(Enum):
    white: "white"
    brown: "brown"
    black: "black"
    blonde: "blonde" #Rubio
    red: "red"


class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=2,
        max_length=50,
        example="Benito Juarez"
    )
    state: str = Field(
        ...,
        min_length=2,
        max_length=50,
        example="Ciudad de Mexico"
    )
    country: str = Field(
        ...,
        min_length=2,
        max_length=50,
        example="Mexico"
    )


class PersonBase(BaseModel):
    first_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Miguel Angel"
    )
    last_name: str = Field(
        ..., 
        min_length=1,
        max_length=50,
        example="Sanchez Quintana"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=20
    )
    #hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=False)
    # email: EmailStr
    # website_url: HttpUrl
    

    # class Config:
    #     schema_extra = {
    #         "example": {
    #         "first_name": "Miguel",
    #         "last_name": "Sanchez",
    #         "age": 20,
    #         #"hair_color": "white",
    #         "is_married": False,
    #         "email": "mike@mail.com",
    #         "website_url": "https://platzi.com",
    #         "password": "root1234"
    #         }
    #     }


class Person(PersonBase):
    password: str = Field(..., min_length=8, example="root1234")


class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="Miguel2022")

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new", response_model=PersonOut, status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get("/person/detail", status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters"
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
    )
):
    return {name: age}

# Validaciones: Path parameters

@app.get("/person/detail/{person_id}", status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(..., gt=0) #obligatorio
):
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put("/person/{person_id}",status_code=status.HTTP_202_ACCEPTED)
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...)
    #location: Location = Body(...)
): 
    #results = person.dict()
    # results.update(location.dict())
    # return results
    return person


@app.post("/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)