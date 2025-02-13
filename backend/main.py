#main.py

from fastapi import FastAPI
from core.config import settings
from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    year: int


class BookUpdate(BaseModel):
    title: str
    author: str
    year: int

class BookPartialUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


books = [
    {'id': 1, 'title': 'The Pragmatic Programmer', 'author': 'Andrew Hunt and David Thomas', 'year': 1999},
    {'id': 2, 'title': 'Clean Code', 'author': 'Robert C. Martin', 'year': 2008},
    {'id': 3, 'title': 'Design Patterns', 'author': 'Erich Gamma', 'year': 1994},
    {'id': 4, 'title': 'Refactoring', 'author': 'Martin Fowler', 'year': 1999},
]

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

@app.get("/books")
def get_all_books():
    return books


@app.get("/books/{book_id}")
def get_single_book(book_id: int):
    
    for book in books:
        if book['id'] == book_id:
            return book

    return JSONResponse(content={"Error!":"Book is not available!"}, status_code=status.HTTP_404_NOT_FOUND)


@app.post("/books")
def create_books(book: BookCreate):
    new_book = {
        'id': len(books)+1,
        'title': book.title,
        'author': book.author,
        'year': book.year
    }

    books.append(new_book)

    return JSONResponse(content={"Success": "Book added successfully"},status_code=status.HTTP_201_CREATED)


@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):
    return JSONResponse(content={"message": "Book updated successfully!"},status_code=status.HTTP_200_OK)


@app.patch("/books/{book_id}")
def partial_update(book_id: int, book: BookPartialUpdate):
    if book.title:
        print("Title updated!")

    if book.author:
        print("Author updated!")

    if book.year:
        print("Year updated!")

    return JSONResponse(content={"message": "Book updated successfully!"}, status_code=status.HTTP_200_OK)


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    return JSONResponse(
        content = {"success": "Book deleted successfully"},
        status_code=status.HTTP_204_NO_CONTENT
    )
