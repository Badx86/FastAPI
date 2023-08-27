from fastapi import FastAPI

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(1, 'Computer Science Pro', 'coding with Roby', 'Great book!', 5),
    Book(2, 'Python Basics', 'pythonista', 'An excellent introduction to Python', 4.8),
    Book(3, 'Web Development Masterclass', 'web guru', 'Guide to web development', 4.0),
    Book(4, 'Machine Learning', 'ml enthusiast', 'Shit book >.<', 3.7),
    Book(5, 'Data Science', 'coding with Roby', 'Recipes for successful analysis', 4.5),
    Book(6, 'Artificial Intelligence', 'ai wizard', 'Exploring the world of AI', 4.7)
]


@app.get("/books")
async def read_all_books():
    return BOOKS
