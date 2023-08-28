from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2025)

    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'Author name',
                'description': 'A new description',
                'rating': 5,
                'published_date': 2023
            }
        }


BOOKS = [
    Book(1, 'Computer Science Pro', 'coding with Roby', 'Great book!', 5, 2021),
    Book(2, 'Python Basics', 'pythonista', 'An excellent introduction to Python', 4, 2022),
    Book(3, 'Web Development Masterclass', 'web guru', 'Guide to web development', 4, 2021),
    Book(4, 'Machine Learning', 'ml enthusiast', 'Shit book >.<', 3, 2020),
    Book(5, 'Data Science', 'coding with Roby', 'Recipes for successful analysis', 2, 2019),
    Book(6, 'Artificial Intelligence', 'ai wizard', 'Exploring the world of AI', 5, 2023)
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


@app.get("/books/publish/")
async def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2025)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)

    return books_to_return


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break