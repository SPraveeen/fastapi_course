from fastapi import FastAPI, Body,Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

class Book:
    id:int
    title:str
    author:str
    description:str
    published_date:int
    rating:int

    def __init__(self,id,title,author,description,published_date,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.published_date=published_date
        self.rating=rating

class BookRequest(BaseModel):
    id:Optional[int] = Field(description='ID is not needed on Create',default=None)
    title:str = Field (min_length=3)
    author:str = Field (min_length=3)
    description:str = Field (min_length=1,max_length=100)
    published_date:int=Field(gt=1999,lt=2031)
    rating:int = Field(gt=0,lt=6)

    model_config={
        'json_schema_extra':{
            'example':{
                'title': ' A new book',
                'author':'coding with roby',
                'description':'a new description of a book',
                'published_date':'2014',
                'rating':5
            }
        }
    }   

BOOKS=[
    Book(1,'cs pro','coding','nice book',2014,5),
    Book(2,'endpoints','coding','great book',2019,5),
    Book(3,'Master endpoints','coding','awesome',2025,5),
    Book(4,'HP1','Author 1','Book Description',2005,2),
    Book(5,'HP2','Author 2','Book Description',1964,3),
    Book(6,'HP3','Author 3','Book Description',1944,1),
]

app=FastAPI()

@app.get('/books',status_code=status.HTTP_200_OK)
async def get_all_books():
    return BOOKS

@app.get('/books/{book_id}',status_code=status.HTTP_200_OK)
async def get_specific_book(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book        
    raise HTTPException(status_code=404,detail='Item not found')

@app.get('/books/',status_code=status.HTTP_200_OK)
async def get_by_rating(book_rating:int=Query(gt=0, lt=6)):
    bookk=[]
    for book in BOOKS:
        if book.rating==book_rating:
            bookk.append(book)
    return bookk

@app.get('/books/publish/',status_code=status.HTTP_200_OK)
async def get_books_by_date(published_date:int=Query(gt=1999,lt=2031)):
    bookk=[]
    for book in BOOKS:
        if book.published_date == published_date:
            bookk.append(book)
    return bookk
        
@app.post('/create-book',status_code=status.HTTP_201_CREATED)
async def create_books(create_new_book:BookRequest):
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

@app.put('/books/update_book',status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id== book.id:
            BOOKS[i] = book
            book_changed=True
    if not book_changed:
        raise HTTPException(status_code=404,detail='Item not found')
    

@app.delete('/books/{books_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_books(books_id:int=Path(gt=0)):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==books_id:
            BOOKS.pop(i)
            book_changed=True
            break
    if not book_changed:
        raise HTTPException(status_code=404,detail='Item not found')

