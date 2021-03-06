# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field, EmailStr, HttpUrl, PositiveInt

# FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import FastAPI, Body, Query, Path, Form, Header, Cookie, UploadFile, File

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

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK,
    tags=["Home"]
)
def home():
    """
    Home

    This path operation show the home page with the posts

    Do not recieve parameters

    Return the message Hello World
    """
    return {"Hello": "World"}

# Request and Response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut, 
    status_code=status.HTTP_201_CREATED,
    tags=["Posts"],
    summary="Create Person in the app"
)
def create_person(person: Person = Body(...)):
    """
    Create Person

    This path operation creates a person in the app and save the information in the database

    Parameters:
    - Request body parameter:
        - **person: Person** -> A model with the first name, last name, age, hair color, and marital status
    
    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail", 
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    deprecated=True
)
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
    """
    Show Person

    This path operation search a user in the data base

    Parameters:
    - Request body parameter:
        - **name: str** -> Recieve the name of the person 
        - **age: int** -> Recieve the age of the person 

    Return the user's name and age.
    """
    return {name: age}

# Validaciones: Path parameters

persons = [1,2,3,4,5]

@app.get(
    path="/person/detail/{person_id}", 
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def show_person(
    person_id: int = Path(..., gt=0) #obligatorio
):
    """
    Show Person
    
    This path operation check if the id was already used

    Parameters:
    - **id: int** -> Recieve the user's id

    Return if the user already exists
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person does not exist."
        )
    return {person_id: "It exists!"}

# Validaciones: Request Body
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Persons"]
)
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
    """
    Update Person

    This path operation update user's information

    Parameters:
    - Request body parameter:
        - **Person: Person** -> A model with the first name, last name, age, hair color, and marital status
    
    Returns the person with his information updated
    """
    #results = person.dict()
    # results.update(location.dict())
    # return results
    return person

# Forms

@app.post(
    path="/login", 
    response_model=LoginOut, 
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def login(
    username: str = Form(...), 
    password: str = Form(...)
):
    """
    Login

    This path allows users login in the app

    Parameters:
    - Response body parameters:
        - **Username: str** 
        - **Password: str**
    
    Returns a succesful login
    """
    return LoginOut(username=username)

# Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["About"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
): 
    """
    Contact

    This path add a cookie on the browser

    Parameters: 
    - Request body parameters:
        - First name, Last name, Email and Message

    Returns the User Agent
    """
    return user_agent

# Files

@app.post(
    path="/post-image",
    tags=["Posts"]
)
def post_image(
    image: UploadFile = File(...)
):
    """
    Post Image

    This path allows to adding a picture to the user

    Parameters:
    - Request body parameters:
        - **Image**
    
    Returns the picture's name, format and size
    """
    return{
        "Filename":image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }