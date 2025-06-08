from fastapi import FastAPI,Body

app=FastAPI()

BOOKS=[
    {'Title':'Title one','Author':'Author one','Subject':'Science'},
    {'Title':'Title two','Author':'Author two','Subject':'Science'},
    {'Title':'Title three','Author':'Author three','Subject':'CP'},
    {'Title':'Title four','Author':'Author four','Subject':'Data'},
    {'Title':'Title five','Author':'Author five','Subject':'Zoology'},
    {'Title':'Title six','Author':'Author two','Subject':'English'}
]


@app.get('/books')
async def read_all_books():
    return BOOKS

@app.get('/books/{book_title}')
async def get_books(book_title:str):
    for book in BOOKS:
        if book.get('Title').casefold()==book_title.casefold():
            return book
        
@app.get('/books/')
async def books_by_category(subject:str):
    books=[]
    for book in BOOKS:
        if book.get('Subject').casefold()==subject.casefold():
            books.append(book)
    return books

@app.get('/books/{author}/')
async def get_book_by_author_categ(author:str,category:str):
    books=[]
    for book in BOOKS:
        if book.get('Author').casefold()==author.casefold() and  book.get('Subject').casefold() == category.casefold():
            books.append(book)
    return books

@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put('/books/update_book')
async def update_book(update_title=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('Title').casefold()==update_title.get('Title').casefold():
            BOOKS[i]=update_title

@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('Title').casefold()==book_title.casefold():
            BOOKS.pop(i)
            break

