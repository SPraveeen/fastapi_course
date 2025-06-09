from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int

    def __init__(self,id,title,author,description,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating

class BookRequest(BaseModel):
    id:Optional[int] = Field(description='ID is not needed on Create',default=None)
    title:str = Field (min_length=3)
    author:str = Field (min_length=3)
    description:str = Field (min_length=1,max_length=100)
    rating:int = Field(gt=0,lt=6)

    model_config={
        'json_schema_extra':{
            'example':{
                'title': ' A new book',
                'author':'coding with roby',
                'description':'a new description of a book',
                'rating':5
            }
        }
    }   

BOOKS=[
    Book(1,'cs pro','coding','nice book',5),
    Book(2,'endpoints','coding','great book',5),
    Book(3,'Master endpoints','coding','awesome',5),
    Book(4,'HP1','Author 1','Book Description',2),
    Book(5,'HP2','Author 2','Book Description',3),
    Book(6,'HP3','Author 3','Book Description',1),
]

app=FastAPI()

@app.get('/books')
def get_all_books():
    return BOOKS

@app.post('/create-book')
def create_books(create_new_book:BookRequest):
    new_book=Book(**create_new_book.model_dump())
    BOOKS.append(find_book_id(new_book))

# to increment id number
def find_book_id(book : Book):
    # book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id+1
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id +1
    else:
        book.id=1
    return book
